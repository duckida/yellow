import os
import openai

openai.api_key = "YOUR_API_KEY_HERE" #replace with an OpenAI API key



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

As an interpreter, you must convert all given Yellow code to Python. You must only return Python code. 
Make sure you import all modules needed. 

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

""",
        }]
    chat_log.append({'role': 'user', 'content': question})
    response = completion.create(model='gpt-3.5-turbo', messages=chat_log)
    answer = response.choices[0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': answer})
    return answer, chat_log

print("Welcome to Yellow v0.1. Ctrl+C to exit\n")
while True:
    yellow_input = input(">>>")
    answer, log = askgpt(yellow_input)
    print(answer)
