import os
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
openai = OpenAI()

OLLAMA_BASE_URL = "http://localhost:11434/v1"
text_msg = "Hi my name is Andy and I like banoffee pie"
gpt_model = "gpt-4.1-mini"
ollama_model = "llama3.2"

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": text_msg}
    ]

messages_followup = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
    ]

messages_full = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": text_msg},
    {"role": "assistant", "content": "Hi Andy! Banoffee pie is delicious—it's such a tasty treat. Do you have a favorite recipe or a special way you like to enjoy it?"},
    {"role": "user", "content": "What's my name?"}
    ]



def main():
    """
    Tokenizer exmple.
    """
    encoding = tiktoken.encoding_for_model(gpt_model)
    tokens = encoding.encode(text_msg)
    #print(tokens)

    for token in tokens:
        print(f"Token: {token} Text: '{encoding.decode([token])}'")


    """
    Calling openai example.
    """
    print(" ")
    print("------------")
    print("OpenAI Sample:")
    api_key = os.getenv("OPENAI_API_KEY")

    #Ollama example
    ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

    
    #response = openai.chat.completions.create(model=gpt_model, messages=messages)
    response = ollama.chat.completions.create(model=ollama_model, messages=messages)
    first_result = response.choices[0].message.content
    print(first_result)
    print(" ")

    #response_followup = openai.chat.completions.create(model=gpt_model, messages=messages_followup)
    response_followup = ollama.chat.completions.create(model=ollama_model, messages=messages_followup)
    followup_result = response_followup.choices[0].message.content
    print(followup_result)  
    print(" ")

    #response_full = openai.chat.completions.create(model=gpt_model, messages=messages_full)
    response_full = ollama.chat.completions.create(model=ollama_model, messages=messages_full)
    full_result = response_full.choices[0].message.content
    print(full_result)


    """
        Reminder, if you want to use Anthropic, here's a code snippet.
        mport anthropic

            client = anthropic.Anthropic(
                api_key="your-anthropic-api-key"
            )

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": "Hello, Claude!"}
                ]
            )
    """


if __name__ == "__main__":
    main()
