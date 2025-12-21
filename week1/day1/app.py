# Setting up python environment:

#   - create folder
#   - run python code:  python -m venv .venv
#   	This sets up the environment, if you want to set it up that way.
#   - go to .venv\Scripts\activate
#	    This sets the virtual environment
#
#   With vscode, hit Ctrl + Shift + P for command pallete.  select:  "Python: Select Interpreter" select the venv
#	    venv is the virtual interpreter.  You can go into there and set up packages and configuration.

#   - here is where you'll run your pip to install packages. Example:
#   python -m pip install python-dotenv openai ipython requests beautifulsoup4
#       beautifulsoup4 is used for screen scrapping.

#   - After that, scraper needs to have a file created, so also created scraper.py and added the reference to it in here.



import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI

# load env file.
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start with the correct prefix.  Please check your OPENAI_API_KEY variable.")
elif api_key.strip() != api_key:    
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


message = "Hello, GPT! This is my first ever message to you! Hi!"
messages = [{"role": "user", "content": message}]

# Creating open AI object
openai = OpenAI()

# sending request and returning the response.
response = openai.chat.completions.create(model="gpt-5-nano", messages=messages)
# getting the response from the response object.
#print(response.choices[0].message.content)



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





def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]

def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    return display(Markdown(summary))



#ed = fetch_website_contents("https://edwarddonner.com")
#messages_for(ed)

#summarize("https://edwarddonner.com")
#print(display_summary("https://edwarddonner.com"))

test_md = Markdown("# Test Header\n\nThis is **bold** text")
print("Type:", type(test_md))
display(test_md)

