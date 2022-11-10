#!/usr/bin/env python3
 
from scapy.all import *
from scapy.modules import *
from scapy import *
from scapy2dict import to_dict
import csv
import os
# a=sniff(count=10)
# a.nsummary()

# send(IP(dst="1.2.3.4")/ICMP())
# sendp(Ether()/IP(dst="1.2.3.4",ttl=(1,4)),
# iface="eth1")

# client_ip = "10.0.3.15"
# # client_MAC = "08:00:27:e9:e6:dd"
# # server_ip = "10.0.3.2"
# server_MAC = "52:54:00:12:35:02"
# hacker_ip = "192.168.56.103"
# # hacker_MAC = "08:00:27:22:46:4f"

# ans,unans=sr(IP(dst=client_ip,ttl=5)/ARP())
# ans.nsummary()
# unans.nsummary()
# p=sr(IP(dst=client_ip)/ARP()/f"Who has {client_ip}. Tell {hacker_ip}")
# p.show()
# ans,unans=sr(IP(dst="192.168.56.101",ttl=5)/ICMP())
# ans.nsummary()
# unans.nsummary()
# p=srp(IP(dst="192.168.56.011")/ARP()/"Who has 192.168.56.101? Tell 192.168.56.103")
# p.show()


# conf.verb = 0
# ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=sys.argv[1]),
#                  timeout=2)

pending_packets = []

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        pending_packets.append(pkt)
        wrpcap('arp_monitor.pcap', pending_packets)  
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

#sniff(prn=arp_monitor_callback, filter="arp", store=0, count=3)
#sniff and store the results in a dictionary


def sniffmgmnt(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2):
        keys = [(pkt.addr3)]
        values = [(pkt.addr1, pkt.addr2)]
        my_dict = dict(zip(keys, values))
        with open('data.csv','a') as f:
                w = csv.writer(f)
                w.writerows(my_dict.items())


# for pkt in list_packets:
#     print(pkt.summary())




# def write_sniffed_arp_packets_to_file():
#     with open('arp_monitor.pcap', 'wb') as f:
#         f.write(sniff(prn=arp_monitor_callback, store=0, filter="arp"))






# sniff(prn=arp_monitor_callback, filter="arp", store=0)

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False)[0]
    return answered_list





# print(dir(scapy))
