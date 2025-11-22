# Beginner's Guide to Networking Projects 

This repository contains three key projects developed to explore, analyze, and visualize fundamental networking concepts. 

---

## 1. Local Traffic Interceptor (ARP Spoofing Tool)

This project uses Python and the Scapy library to place our machine secretly between a router and another device to monitor their traffic.

### The Problem:  Accessing Other Devices' Data

Normally, your network card only accepts packets addressed specifically to its unique hardware ID (the **MAC Address**). All other traffic is ignored, making it impossible to "eavesdrop."

### The Solution:  Faking Identities (ARP Spoofing)

We exploit the network's address book, called **ARP**, by constantly sending false messages. We lie to the network by pretending to be the router for the victim and the victim for the router. This forces all traffic between them to pass through our machine first.

### Key Concepts Taught

| Concept | What It Is & What It Teaches |
| :--- | :--- |
| **ARP Spoofing** | **Faking identities** on the network. Teaches how easily this protocol can be manipulated. |
| **IP Forwarding** | A Linux setting that turns our computer into a **temporary router**. Teaches how operating systems handle traffic meant for other machines. |
| **Promiscuous Mode** | Setting the network card to **accept all packets** it sees. Teaches the initial hurdle to network monitoring. |
| **Packet Forwarding** | The crucial step of **logging the data** and then correctly sending the packet to its original destination to keep the connection alive. |

---

## 2. Real-Time "Traffic Light" Latency Monitor (CLI Tool)

This Python application diagnoses slow network performance by checking three separate stages of a connection and instantly showing where the bottleneck is.

### The Problem:  Isolating Slow Performance

When the internet is slow, it's difficult to know *why*: Is it my Wi-Fi? My internet provider (ISP)? Or a server on the other side of the world?

### The Solution:  Color-Coded Tiers

The tool uses simultaneous tests (via `ping` commands) against three distinct network tiers and translates the response time (**latency**) into a clear **Green** (Good), **Yellow** (Warning), or **Red** (Bad) status.

### Key Concepts Taught

| Concept | What It Is & What It Teaches |
| :--- | :--- |
| **Latency & Ping** | **Latency** is the delay in sending/receiving data. **Ping** is the test used to measure it. Teaches how to quantify network speed. |
| **Network Tiers** | Separates the network into three segments: **Tier 1 (LAN/Router)**, **Tier 2 (ISP Gateway)**, and **Tier 3 (Global DNS)**. Teaches the logical path data takes to leave the home network. |
| **Layer 3 (IP) Analysis** | Focuses on testing the **IP routing** ability of different hops. Teaches fundamental network diagnostics and troubleshooting. |

---

## 3. Traffic Simulator 

A browser-based simulation that visually shows how data packets travel across a network path.

### The Problem:  Abstract Networking Concepts

Ideas like **hops**, **latency**, and **queuing** (waiting in line) are hard to visualize, making them difficult for beginners to grasp.

### The Solution:  See the Packets Travel

The tool creates a path of virtual nodes (like computers or routers) and allows you to watch data packets travel between them. You can adjust the delay for each node to see how even small delays add up to big performance issues.

### Key Concepts Taught

| Concept | What It Is & What It Teaches |
| :--- | :--- |
| **Hops & Routing** | **Hops** are the number of nodes a packet crosses to reach its destination. Teaches how data moves step-by-step through a network path. |
| **Queuing & Latency** | **Queuing** is when packets have to wait for a busy node. Teaches that network delay (**latency**) isn't just travel time but also waiting time. |
| **Visualization** | The visual approach makes abstract data concepts **concrete** and allows for instant experimentation (e.g., doubling the delay to see the result). |
