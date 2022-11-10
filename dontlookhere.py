#!/usr/bin/env python3
import requests
import argparse
import sys
import random



def read_wordlist(wordlist):
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

def construct_payload(url, wordlist):
        for word in wordlist:
            payload = url.replace('fuzz', word)
            print('\n'f'Fuzzing with {payload}')
            response = requests.get(payload)
            if response.status_code != 200:
                print(f'Error: {response.status_code} from {payload}')
            else:
                print(f'Success: {response.status_code} from {payload}')
                print(response.headers)

def main():
    url = input("What URL do you want to use? (Format in the style of http(s)://www.yoururlhere.com/?yourparameter=FUZZ")
    wordlist = input("What wordlist do you want to use?")
    construct_payload(url, read_wordlist(wordlist))

if __name__ == '__main__':
    main()