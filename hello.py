import time
import random

print("hello" + "world")
world = "world"
print(f'hello {world}')

def saypartshello():
    text = "helloworld"
    newtext = ""
    for i in range(0, len(text)):
        newtext += text(random.randint(0, len(text)))
    return newtext

def say_hello():
    time.sleep(100)
    print("hello world")
        

def main():
    say_hello()
    saypartshello()

if __name__ == "__main__": 
    main()