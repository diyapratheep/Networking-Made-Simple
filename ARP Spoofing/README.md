# Local Traffic Interceptor (ARP Spoofing Tool)

This project is a simple Python Command Line Interface (CLI) tool built to intercept network traffic between two devices on a local network (such as your home Wi-Fi). It demonstrates fundamental networking concepts like ARP, IP routing, and packet forwarding.

---

##  The Problem: Why Can't I See Other People's Traffic?

Normally, when you connect to a network, your computer only looks at data packets specifically addressed to its unique hardware ID (MAC Address). All other traffic is ignored by your network card.

### Goal  

We need a way to trick two devices (like a router and a phone) into sending all their data traffic through our machine so we can monitor it.

---

##  The Solution: Trick the Network with ARP Spoofing

The solution is to abuse a core, insecure mechanism of local networks called **ARP (Address Resolution Protocol)**.

### Key Networking Concepts

| Jargon Term | Simple Meaning | Why We Use It |

|------------|----------------|----------------|

| **ARP** | A protocol that maps an IP Address (e.g., 192.168.1.50) to a MAC Address (hardware ID). | It's easily tricked. We send fake ARP messages. |

| **ARP Spoofing** | Sending false ARP messages to redirect traffic. | We pretend: "I am the Router" to the phone, and "I am the Phone" to the router. |

| **IP Forwarding** | A setting in Linux that allows passing through packets not meant for this machine. | Lets our machine act like a temporary router. |

| **Promiscuous Mode** | Network card accepts all packets it sees. | Ensures we capture redirected traffic. |

| **Scapy** | Python library to create and analyze packets. | Used to craft fake ARP packets and sniff traffic. |

---

## 🛠️ Getting Started (Prerequisites)

This project requires a **Linux environment** (like Ubuntu running inside VirtualBox or VMware).

---

## 1. Configure the Environment

### 🔧 Virtual Machine (VM) Network

Set your VM's network adapter to:

```
Bridged Mode
```

This ensures the VM receives a valid IP address on your local network.

---

## 2. Install Dependencies

Run these commands:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip install scapy
```

---

## 3. Enable IP Forwarding

Enable packet forwarding in Linux:

```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

---

##  How to Run the Tool

The tool uses **two separate terminal windows**:

* one for the ARP spoofing attack loop

* one for sniffing (packet monitoring)

---

##  Terminal 1: The Attack Loop (Spoofing)

This script **must run continuously** to maintain the man-in-the-middle position.

```bash
sudo python3 arp_spoof.py

```

---

##  Terminal 2: The Monitoring Loop (Sniffing)

Open a Python shell with root privileges:

```bash

sudo python3

```

Then enter:

```python

import scapy.all as scapy
from arp_spoof import process_packet
scapy.sniff(filter="tcp port 80", prn=process_packet, store=0)

```

This listens for redirected traffic coming through your machine.

---

##  What You Learn From This Project

* How ARP works and why it's insecure

* How devices identify each other using MAC and IP

* How to forward packets using Linux

* How attackers position themselves between two devices

* How to sniff and analyze redirection traffic

* Why HTTPS prevents sniffing


---

## ⚠️ Legal & Ethical Disclaimer

This project is created for **educational purposes only**.

Do NOT use it on networks or devices you do not own or have explicit permission to test.

Unauthorized interception of network traffic is **illegal**.
