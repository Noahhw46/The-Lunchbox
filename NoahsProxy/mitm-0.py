import sys

def request(context, flow):
  f = open('httplogs.txt', 'w')
  f.write(flow.request.url + '\n') 
  f.close()