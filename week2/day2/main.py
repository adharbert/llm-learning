import os
import questions as gr
from dotenv import load_dotenv
from openai import OpenAI
import webbrowser
import time

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

openai = OpenAI()

anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

anthropic = OpenAI(api_key=anthropic_api_key, base_url=anthropic_url)
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

system_message = "You are a helpful assistant"


force_dark_mode = """
function() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.replace(url.href);
    }
}
"""



def message_gpt(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content

def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()


def main():
    #today_date = message_gpt("What is today's date?")
    #print(today_date)

    # # basic gradio interface
    # gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch()

    # Adding share=True means that it can be accessed publically
    # A more permanent hosting is available using a platform called Spaces from HuggingFace, which we will touch on next week
    # NOTE: Some Anti-virus software and Corporate Firewalls might not like you using share=True. 
    # If you're at work on on a work network, I suggest skip this test.
    #gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)

    #gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never", js=force_dark_mode).launch()
    #gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(js=force_dark_mode)

    app = gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never")
    app.launch(inbrowser=False, prevent_thread_lock=True)
    
    # Small delay to ensure server is up
    time.sleep(1)

    # Open browser with dark theme parameter
    webbrowser.open("http://127.0.0.1:7861/?__theme=dark")

    # use this to keep the app running
    app.block_thread()



if __name__ == "__main__":
    main()
