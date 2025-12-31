import os
import questions as gr
from dotenv import load_dotenv
from openai import OpenAI
import webbrowser
import time


def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1


def main():
    for number in count_up_to(5):
        print(number)
    



if __name__ == "__main__":
    main()