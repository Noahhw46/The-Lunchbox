#!/usr/bin/env python3

import requests
import sys 


#usage: python3 buster.py <url> <wordlist>

url = sys.argv[1]
wordlist = sys.argv[2]

with open(wordlist, 'r') as f:
    all_lines = f.readlines()
    
for line in all_lines:
        line = line.strip()
        response = requests.get(f"{url}/{line}")
        try:
            response.raise_for_status()
            response = response.text
            print(f'{url}/{line}')
        except:
            print(f"{response} from {url}/{line}")


