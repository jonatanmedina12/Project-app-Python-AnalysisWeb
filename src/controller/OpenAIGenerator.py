from openai import OpenAI

from dotenv import load_dotenv

import tkinter as tk

from tkinter import filedialog

load_dotenv()


class OpenAIGenerator:
    def __int__(self,model_name='gtp-0-0125-preview'):
        self.client = OpenAI()
        self.model_name=model_name

    def generate(self,prompt):
        reponse = self.client.chat.completions.create(
            mens
        )