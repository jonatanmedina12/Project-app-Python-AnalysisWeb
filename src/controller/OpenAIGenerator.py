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
        response = self.client.chat.completions.create(
            messages=[{'role':"user","content":prompt}],
            model=self.model_name
        )
        return response.choices[0].message.content

def generate_oneliner(generator,prompt,code):

    prompt =f"{prompt}:\n{code}"
    try:
        return generator.generate(prompt)
    except Exception as e:
        print(f"Error al generar el onliner {e}")

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return  file_path


if __name__ =="__main__":
    file_path = select_file()
    if file_path:
        with open(file_path) as file:
            content = file.read()
        generator = OpenAIGenerator()
        prompt =""
        oneliner = generate_oneliner(generator,prompt,content)
        print(oneliner)
