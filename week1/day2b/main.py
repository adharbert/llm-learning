import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')


""" 
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
else:
    print("API key found and looks good so far!") 
"""
print("")
print("")

# URLs
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
PROMPT = "Tell me a fun fact about Hubble Space Telescope."


# Gemini using OpenAI SDK
gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
responseG = gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=[{"role": "user", "content": PROMPT}])
print(responseG.choices[0].message.content)
print("-----")
print("")


# Ollam local
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')    
responseO = ollama.chat.completions.create(model="llama3.2", messages=[{"role": "user", "content": PROMPT}])
print(responseO.choices[0].message.content)
print("-----")
print("")

print("Done!")

