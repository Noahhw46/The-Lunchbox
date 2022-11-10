#!/usr/bin/env python3
import requests
# import random ###FOR TESTING PURPOSES###



def read_wordlist(wordlist):
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

def construct_payload(url, wordlist):
        for word in wordlist:
            payload = url.replace('FUZZ', word)
            print('\n'f'Fuzzing with {payload}')
            response = requests.get(payload)
            if response.status_code != 200:
                print(f'Error: {response.status_code} from {payload}')
            else:
                print(f'Success: {response.status_code} from {payload}')
                print(response.headers)

def main():
    url = input(f"What URL do you want to use? (Use 'FUZZ' for fuzzing. Ex: http(s)://www.yoururlhere.com/?yourparameter=FUZZ):\n")
    wordlist = input(f"What wordlist do you want to use? (Full or relative path to word list):\n")
    construct_payload(url, read_wordlist(wordlist))

if __name__ == '__main__':
    main()