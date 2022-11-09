#!/usr/bin/env python3

import requests
import sys 

params = {}
with open('wordlist.txt', 'r') as f:
    lines = f.readlines()
    lines = lines.strip()
    for line in lines:
        params[line] = ["true"]


url = sys.argv[1]
response = requests.get(url="", params="")
