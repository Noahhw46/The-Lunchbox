#!/usr/bin/env python3
 
from scapy.all import *
from scapy.modules import *
from scapy import *
from scapy2dict import to_dict
import PacketReader



#Sniffing all broadcast packets

pending_packets = []

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        pending_packets.append(pkt)
        wrpcap('mitm_attack/arp_monitor.pcap', pending_packets)  
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")


def sniff():
    sniff(prn=arp_monitor_callback, filter="arp", store=0, count=3)



#Extracting the MAC and IP addresses from the sniffed packets
def read_bytes_from_pcap():
    packets = rdpcap('mitm_attack/arp_monitor.pcap')
    packet_dict = {}
    packet_dict = {packet[ARP].hwsrc: [packet[ARP].psrc, packet[ARP].pdst] for packet in packets}
    print(packet_dict)



read_bytes_from_pcap()