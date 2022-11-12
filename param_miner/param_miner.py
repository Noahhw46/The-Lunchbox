#!/usr/bin/env python3

import requests
import random
import time
import regex as re



def extract_parms(response):
    #split the response into a list by line
    response = response.splitlines()
    params = r"(\?|&)([^=]+)="
    all_params_uris = [url for url in response if re.search(params, url)]

    final_uris = []
    for uri in all_params_uris:
        delim = uri.find("=") + 1
        final_uri = uri[:delim] + 'FUZZ'
        final_uris.append(final_uri)
    
    
    final_uris = list(set(final_uris))
    return final_uris

    

def makerequest(domain):
    result = False
    with open('wordlists/useragents.txt', 'r') as f:
        agents = f.readlines()
        agents = [agent.strip() for agent in agents]
    agent = random.choice(agents)

    headers = {'User-Agent': agent}

    url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

    try:
        response = requests.get(url, headers=headers, timeout=40)
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
    domain = input("What domain would you like to mine from? ")
    print(f"Extracting parameters from {domain}")
    fle = input("What file would you like to save the results to? ")
    res = makerequest(domain)
    if res:
        extracted = extract_parms(res)
        with open('param_miner/' + fle, 'w') as f:
            for uri in extracted:
                f.write(uri + '\n')
        print(f"Found {len(extracted)} parameters. Output written to param_miner/{fle}")
    else:
        print("No parameters found.")
    






if __name__ == '__main__':
    main()