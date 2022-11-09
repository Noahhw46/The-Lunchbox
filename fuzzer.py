#!/usr/bin/env python3
import requests
import argparse
import sys
import random
#a simple tool to fuzz a web application

#first we need to parse the arguments
def parse_args():
    parser = argparse.ArgumentParser(description='A simple tool to fuzz a web application, use keyword "fuzz" to define fuzzing points, or use -p to define the parameters to fuzz')
    parser.add_argument('-u', '--url', help='The url to fuzz', required=True)
    parser.add_argument('-w', '--wordlist', help='The wordlist to use', required=True)
    parser.add_argument('-p', '--params', help='The parameters to fuzz', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    return args

#now we need to read the wordlist
def read_wordlist(wordlist):
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

#now we need to construct the payload
def construct_payload(url, params, wordlist, args):
    params = params.split(',')
    if len(params) > 1:
        for param in params:
            for word in wordlist:
                payload = url.replace(param, word)
                if args.verbose:
                    print(f'Fuzzing with {payload}')
                response = requests.get(payload)
                if response.status_code != 200:
                    print(f'Error: {response.status_code} from {payload}')
    else:
        for word in wordlist:
            payload = url.replace('fuzz', word)
            if args.verbose:
                print(f'Fuzzing with {payload}')
            response = requests.get(payload)
            if response.status_code != 200:
                print(f'Error: {response.status_code} from {payload}')

def read_wordlist(wordlist):
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

def main():
    args = parse_args()
    wordlist = read_wordlist(args.wordlist)
    if args.params:
        construct_payload(args.url, args.params, wordlist, args)
    else:
        construct_payload(args.url, 'fuzz', wordlist, args)