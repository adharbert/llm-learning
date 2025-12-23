import os
import json
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI
from anthropic import Anthropic

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

openai_model = 'gpt-5-nano'
anthropic_model = 'claude-sonnet-4-5-20250929'

testsite_url = "https://devblogs.microsoft.com/dotnet/"

openai = OpenAI()
claude = Anthropic()


link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""



def get_links_user_prompt(url):
    user_prompt = f"""
    Here is the list of links on the website {url} -
    Please decide which of these are relevant web links for a brochure about the company, 
    respond with the full https URL in JSON format.
    Do not include Terms of Service, Privacy, email links.

    Links (some might be relative links):

    """
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


def select_relevant_links_openai(url):
    response = openai.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    results = response.choices[0].message.content
    links = json.loads(results)
    return links

def fetch_page_and_all_relevant_links_openai(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links_openai(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result





def select_relevant_links_claude(url):
    response = claude.messages.create(
        model=anthropic_model,
        system=link_system_prompt,
        messages= [{"role": "user", "content": get_links_user_prompt(url)}],        
        max_tokens=1000
    )
    results = response.content[0].text
    print(results)
    return results

def fetch_page_and_all_relevant_links_claudei(url):
    contents = fetch_website_contents(url)
    relevent_links = select_relevant_links_claude(url)

    # If it's already a dict, don't parse it
    try:
        # It was weird, claude kept returning data wrapped in ```json ... ```, added this clean method to fix it.
        relevent_links_clean = clean_json_response(relevent_links)
        relevent_links_dict = json.loads(relevent_links_clean)
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        print(f"Error at position {e.pos}: {relevent_links[max(0, e.pos-20):e.pos+20]}")
        raise

    #relevent_links_dict = json.loads(relevent_links)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    
    for link in relevent_links_dict['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result


def clean_json_response(text):
    text = text.strip()
    
    # Remove ```json and ``` markers
    if text.startswith('```'):
        # Find the first newline after ```
        first_newline = text.find('\n')
        if first_newline != -1:
            text = text[first_newline + 1:]
        
        # Remove trailing ```
        if text.endswith('```'):
            text = text[:-3]
    
    return text.strip()



def main():
    # links = select_relevant_links_openai(testsite_url)
    # claudel_links = select_relevant_links_claude(testsite_url)
    #openai_links = fetch_page_and_all_relevant_links_openai(testsite_url)
    #print(openai_links)

    cloaud_links = fetch_page_and_all_relevant_links_claudei(testsite_url)
    print(cloaud_links)
    

    print("All done!")

if __name__ == "__main__":
    main()
