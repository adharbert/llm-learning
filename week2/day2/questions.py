import os
from dotenv import load_dotenv
from openai import OpenAI
import webbrowser
import time
import gradio as gr

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

openai = OpenAI()

anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

anthropic = OpenAI(api_key=anthropic_api_key, base_url=anthropic_url)
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

system_message = "You are a helpful assistant that responds in markdown without code blocks"



def stream_model(prompt, model):
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="Claude":
        result = stream_claude(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result


def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def stream_claude(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = anthropic.chat.completions.create(
        model='claude-sonnet-4-5-20250929',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def main():
    
    message_input = gr.Textbox(label="Your message:", info="Enter a message for the LLM", lines=7)
    model_selector = gr.Dropdown(["GPT", "Claude"], label="Select model", value="GPT")
    message_output = gr.Markdown(label="Response:")

    view = gr.Interface(
        fn=stream_model,
        title="LLMs", 
        inputs=[message_input, model_selector], 
        outputs=[message_output], 
        examples=[
                ["Explain the Transformer architecture to a layperson", "GPT"],
                ["Explain the Transformer architecture to an aspiring AI engineer", "Claude"],
                ["Explain the theory of relativity to a layperson", "GPT"],
                ["Explain the theory of relativity to a physics student", "Claude"]                
            ], 
        flagging_mode="never"
        )
    view.launch(inbrowser=True)
    
    # use this to keep the app running
    view.block_thread()



if __name__ == "__main__":
    main()