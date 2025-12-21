import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI
from anthropic import Anthropic


# load env file.
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

""" 
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start with the correct prefix.  Please check your OPENAI_API_KEY variable.")
elif api_key.strip() != api_key:    
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!") 
"""


# Setting up prompts
system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""

# Creating open AI object
openai = OpenAI()

anthropic = Anthropic()


# -------------- Methods ------------------

def messages_for(website):
    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Please summarize the following website content:\n\n{website}"
        }
    ]    

def mesages_for_anthropic(input_text):
    return [
        {
            "role": "user",
            "content": f"Please summarize the following website content:\n\n{input_text}"
        }
    ]

def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content



def sumarize_anthropic(url):
    website = fetch_website_contents(url)
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929", #"claude-2",
        system=system_prompt,
        messages = mesages_for_anthropic(website),
        max_tokens=1000
    )
    return response.content[0].text


def display_suamary(url):
    summary = sumarize_anthropic(url) # summarize(url)
    # display is for Cursor/UV
    #display(Markdown(summary))
    print(summary)

# ---------------- End of Methods ------------------


# Call methods.
#display_suamary("https://edwarddonner.com")

print("-----")
display_suamary("https://www.espn.com/nfl/story/_/id/47324625/ranking-nfl-head-coach-potential-openings-2026-season-best-worst-jobs")

      



# message = "Hello, GPT! This is my first ever message to you! Hi!"
# messages = [{"role": "user", "content": message}]



# sending request and returning the response.
# response = openai.chat.completions.create(model="gpt-5-nano", messages=messages)
# getting the response from the response object.
#print(response.choices[0].message.content)

# print(response.choices[0].message.content)

# ed = fetch_website_contents("https://edwarddonner.com")
# print(ed)

# messages_for(ed)



print("End of app.py")
