#!/usr/bin/env python3
import requests
import concurrent.futures
import time
# import random ###FOR TESTING PURPOSES###



def read_wordlist(wordlist):
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

def construct_payload(url, wordlist):
        payloads = []
        for word in wordlist:
            payload = url.replace('FUZZ', word)
            payloads.append(payload)
        return payloads

def send_request(payload):
    response = requests.get(payload)
    if response.status_code != 200:
        print(f'Error: {response.status_code} from {payload}')
    else:
        print(f'Success: {response.status_code} from {payload}')
        print(response.headers)

def main():
    url = input(f"What URL do you want to use? (Use 'FUZZ' for fuzzing. Ex: http(s)://www.yoururlhere.com/?yourparameter=FUZZ):\n")
    wordlist = input(f"What wordlist do you want to use? (Full or relative path to word list):\n")

    start = time.perf_counter()
    wordlist = read_wordlist(wordlist)
    payloads = construct_payload(url, wordlist)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, payloads)

    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')

if __name__ == '__main__':
    main()