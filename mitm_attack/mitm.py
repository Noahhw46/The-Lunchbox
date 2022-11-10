#!/usr/bin/env python3
 
from scapy.all import *
from scapy.modules import *
from scapy import *
from scapy2dict import to_dict
import csv
import os



pending_packets = []

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        pending_packets.append(pkt)
        wrpcap('arp_monitor.pcap', pending_packets)  
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")


sniff(prn=arp_monitor_callback, filter="arp", store=0, count=3)