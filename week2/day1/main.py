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

# if openai_api_key:
#     print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
# else:
#     print("OpenAI API Key not set")
    
# if anthropic_api_key:
#     print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
# else:
#     print("Anthropic API Key not set (and this is optional)")

# if google_api_key:
#     print(f"Google API Key exists and begins {google_api_key[:2]}")
# else:
#     print("Google API Key not set (and this is optional)")

# if deepseek_api_key:
#     print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
# else:
#     print("DeepSeek API Key not set (and this is optional)")

# if groq_api_key:
#     print(f"Groq API Key exists and begins {groq_api_key[:4]}")
# else:
#     print("Groq API Key not set (and this is optional)")

# if grok_api_key:
#     print(f"Grok API Key exists and begins {grok_api_key[:4]}")
# else:
#     print("Grok API Key not set (and this is optional)")

# if openrouter_api_key:
#     print(f"OpenRouter API Key exists and begins {openrouter_api_key[:3]}")
# else:
#     print("OpenRouter API Key not set (and this is optional)")


print(" ")
print(" ")
openai = OpenAI()
# For Gemini, DeepSeek and Groq, we can use the OpenAI python client
# Because Google and DeepSeek have endpoints compatible with OpenAI
# And OpenAI allows you to change the base_url

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


## Veriables.
tell_a_joke = [
    {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"},
]


easy_puzzle = [
    {"role": "user", "content": 
        "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only."},
]


hard = """
On a bookshelf, two volumes of Pushkin stand side by side: the first and the second.
The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick.
A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume.
What distance did it gnaw through?
"""
hard_puzzle = [
    {"role": "user", "content": hard}
]



def main():

    ## ------------- Joke prompt ----------------
    ##tell a joke with OpenAI
    #response = openai.chat.completions.create(model="gpt-4.1-mini", messages=tell_a_joke)
    #print(response.choices[0].message.content)


    ## ------------- Easy Puzzle prompt ----------------
    # reasoning effort is newer with GPT-5, has 4 options: "minimal", "low", "medium", "high"
    # Minimal tries to make it as fast as a chat model.

    ## small model with minimal reasoning effort
    # response = openai.chat.completions.create(model="gpt-5-nano", messages=easy_puzzle, reasoning_effort="minimal")
    # print("Minimal effort response")
    # print(response.choices[0].message.content)

    ## small model with low reasonin effort -- results are correct here.
    # response = openai.chat.completions.create(model="gpt-5-nano", messages=easy_puzzle, reasoning_effort="low")
    # print("Low effort")
    # print(response.choices[0].message.content)
    

    ## What if we switch to next model size up with minimaol reasoning effort.
    ## this one is correct as well.
    # response = openai.chat.completions.create(model="gpt-5-mini", messages=easy_puzzle, reasoning_effort="minimal")
    # print(" ")
    # print("GPT-5-mini with minimal effort")
    # print(response.choices[0].message.content)


    ## ------------- Hard Puzzle prompt ----------------
    response = openai.chat.completions.create(model="gpt-5-nano", messages=hard_puzzle, reasoning_effort="minimal")
    print("----------------------- first test -----------------------") 
    print("GPT-5-nano with minimal effort on hard puzzle")
    print(response.choices[0].message.content)
    print(" ")

    response = anthropic.chat.completions.create(model="claude-sonnet-4-5-20250929", messages=hard_puzzle)
    print("----------------------- Second test -----------------------")
    print("Anthropic Claude Sonnet on hard puzzle")
    print(response.choices[0].message.content)
    print(" ")

    print("----------------------- Third test -----------------------")
    response = openai.chat.completions.create(model="gpt-5", messages=hard_puzzle)
    print(" ")
    print("GPT-5 on hard puzzle")
    print(response.choices[0].message.content)
    print(" ")

    print("----------------------- Fourth test -----------------------")
    response = gemini.chat.completions.create(model="gemini-3-pro-preview", messages=hard_puzzle)
    print(" ")
    print("Gemini 3 pro on hard puzzle")
    print(response.choices[0].message.content)



if __name__ == "__main__":
    main()
