import time
from gpt4all import GPT4All

model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
start = time.time()
response = model.generate("who are you ")
print(response)
print("Time taken:", time.time() - start)