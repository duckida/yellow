import os
import openai
import argparse
import platform
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str)
openai.api_key = "Add your OpenAI API key here" # you must add an OpenAI API key for yellow to work.
args = parser.parse_args()
filename = args.file
completion = openai.ChatCompletion()

def askgpt(question, chat_log=None):
    if chat_log is None:
        chat_log = [{
            'role': 'system',
            'content': """There is a new programming language which uses simple terms instead of syntax code. The language is called Yellow.
            An example code in Yellow looks like this:
            'say Hi
            sleep 1 second
            say bye'
            This translates in Python 3 to
            'import time
            print('Hi')
            time.sleep(1)
            print('bye')'
            As an interpreter, you must convert all given Yellow code to Python. You must and can only return Python code. The machine being used is %s.
            Make sure you import all modules needed. The code will be used in production as returned so you must not say anything but the code asked for.
            Example:
            User:
            say Hola
            generate a random number
            say the number
            Interpreter:
            import random
            print('Hola')
            number = random.randint(0, 100)
            print(number)
            User: clear the screen via terminal, say hi
            Interpreter:
            from os import system
            os.system("clear") # if on Windows use cls
            print("hi")
            """ % platform.platform(),
        }]
    chat_log.append({'role': 'user', 'content': question})
    response = completion.create(model='gpt-3.5-turbo', messages=chat_log)
    answer = response.choices[0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': answer})
    return answer, chat_log

if filename == None:
    print("Welcome to Yellow v0.1. Ctrl+C to exit\n")
    while True:
        yellow_input = input(">>>")
        answer, log = askgpt(yellow_input)
        print(answer)
else:
    f = open(filename, "r")
    fdata = f.read()
    c = open('cache.py', 'w+')
    #c.truncate(0)
    answer, log = askgpt(fdata)
    c.write(answer)
    c.close() # need to close the file before executing it
    output = subprocess.check_output("python3 cache.py", shell=True)
    print(output.decode())
