#!/bin/usr/env python3

#send a simple request to google.com and print response

import requests

response = requests.get('https://google.com')
print(response)