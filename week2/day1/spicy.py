import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
grok_api_key = os.getenv('GROK_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')


print(" ")
print(" ")
openai = OpenAI()

anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
deepseek_url = "https://api.deepseek.com"
groq_url = "https://api.groq.com/openai/v1"
grok_url = "https://api.x.ai/v1"
openrouter_url = "https://openrouter.ai/api/v1"
ollama_url = "http://localhost:11434/v1"

anthropic = OpenAI(api_key=anthropic_api_key, base_url=anthropic_url)
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)
deepseek = OpenAI(api_key=deepseek_api_key, base_url=deepseek_url)
groq = OpenAI(api_key=groq_api_key, base_url=groq_url)
grok = OpenAI(api_key=grok_api_key, base_url=grok_url)
openrouter = OpenAI(base_url=openrouter_url, api_key=openrouter_api_key)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)

dilemma_prompt = """
You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:
Cooperate: Choose "Share" — if both of you choose this, you each win $1,000.
Defect: Choose "Steal" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.
If both steal, you both get nothing.
Do you choose to Steal or Share? Pick one.
"""

dilemma = [
    {"role": "user", "content": dilemma_prompt},
]





def main():
    print(" ")

    print("Start Anthropic")
    response = anthropic.chat.completions.create(model="claude-sonnet-4-5-20250929", messages=dilemma)
    print("Anthropic Claude Response:")
    print(response.choices[0].message.content)
    print(" ")

    print("Start GroQ")
    response = groq.chat.completions.create(model="openai/gpt-oss-120b", messages=dilemma)
    print("Groq Response:")
    print(response.choices[0].message.content)
    print(" ")

    print("Start Grok")
    response = grok.chat.completions.create(model="grok-4", messages=dilemma)
    print("Grok Response:")
    print(response.choices[0].message.content)
    print(" ")

    print("Start Gemini")
    response = gemini.chat.completions.create(model="gemini-3-pro-preview", messages=dilemma)
    print("Gemini Response:")
    print(response.choices[0].message.content)
    print(" ")


if __name__ == "__main__":
    main()