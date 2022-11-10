#!/usr/bin/env python3

import requests
import random
import time
import regex as re


def extract_parms(url, placeholder):
    #regex to extract parameters
    params = rf"(\?|&)([^=]+)={placeholder}"
    result = re.findall(params, url)
    return result

def makerequest(url):

    with open('wordlists/useragents.txt', 'r') as f:
        agents = f.readlines()
        agents = [agent.strip() for agent in agents]
    agent = random.choice(agents)

    headers = {'User-Agent': agent}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.text
        
    except requests.exceptions.ConnectionError as e:
            print("Can not connect to server.")
    except requests.exceptions.Timeout as e:
            print("Timeout Error.")
            time.sleep(2)
    except requests.exceptions.HTTPError as err:
            print(f"{err}. Retrying in 2 seconds.")
            time.sleep(2)
    except requests.exceptions.RequestException as e:
            print(" {e} Can not get target information")
    except KeyboardInterrupt as k:
            print("Interrupted by user. Exiting.")
            raise SystemExit(k)    
    finally:
        return result




def main():
    domain = input("What domain would you like to mine from? \n")
    outfile = input("What output file would you like to use? \n")
    placeholder = input("What string as a placeholder after the parameter would you like to use? \n")

    url =  f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey&page=/"






if __name__ == '__main__':
    main()