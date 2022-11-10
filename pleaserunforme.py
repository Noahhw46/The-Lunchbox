#!/usr/bin/env python3

import requests
import sys 
import regex as re

#usage: python3 buster.py <url> <wordlist>



def extract_parms(url, placeholder):
    params = rf"(\?|&)([^=]+)={placeholder}"
    result = re.findall(params, url)
    return result
    
print(extract_parms("https://google.com/?qqwe=fuzz&badsasd=fuzz&badsasd=fuzz&badsasd=fuzz&badsasd=fuzz&badsasd=fuzz&badsasd=fuzz", "fuzz"))