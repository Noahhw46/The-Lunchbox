import random
import os

def russian_roulette():
    if random.randint(0,6) == 1:
        if 'c:' in os.getcwd():
            print('You are dead')
    else:
        print('You are alive')

russian_roulette()