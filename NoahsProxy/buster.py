#!/usr/bin/env python3

import requests
import sys 


#usage: python3 buster.py <url> <wordlist>

#protocol = input(f"Do you want HTTP or HTTPS?\n").lower() ###POSSIBLY UNNEEDED. IT'S HERE INCASE
name_file = input("What would you like to name your output file? Leave empty for none:\n")
url = input(f"What URL are we busting today?\n").lower()
if 'www.' not in url:
    url = f"www.{url}"
    if 'http' not in url:
        url = f"https://{url}"
wordlist = input(f"What is the word list you want to use? (Full or Relative path to word list):\n")


with open(wordlist, 'r') as f:
    all_lines = f.readlines()
    
for line in all_lines:
        line = line.strip()
        response = requests.get(f"{url}/{line}")
        tosave_successes = []
        tosave_failures = []
        try:
            response.raise_for_status()
            response = response.text
            print(f'{url}/{line}')
            tosave_successes.append(f'{url}/{line}')
        except:
            print(f"{response} from {url}/{line}")
            tosave_failures.append(f"{response} from {url}/{line}")

if name_file != "":
    with open(f'{name_file}_successes.txt', 'w') as f:
        for item in tosave_successes:
            f.write(f"{item}\n")

    with open(f'{name_file}_failures.txt', 'w') as f:
        for item in tosave_failures:
            f.write(f"{item}\n")
        
cont = input("Would you like to mine this bust?")


