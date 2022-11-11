#!/bin/usr/env python3

import requests

def bust(url, wordlist, succesful_urls):
    for word in wordlist:
        response = requests.get(f"{url}/{word}")
        http_code = response.status_code
        if 400 <= http_code < 500:
            print(f'{http_code}: {url}/{word}')
        else:
            print(f'{http_code}: {url}/{word}')
            succesful_urls.append(f'{url}/{word}')
            bust(f'{url}/{word}', wordlist, succesful_urls)

    return succesful_urls
    


def main():
    url = input("Enter a url: ")
    succesful_urls = []
    successes = bust(url, open("wordlists/test_wordlist.txt", "r").read().splitlines(), succesful_urls)
    with open('busted_urls.txt', "w") as f:
        for url in successes:
            f.write(url)

if __name__ == "__main__":
    main()
    