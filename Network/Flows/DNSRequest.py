from scapy.all import *

import socket

import sys

server_ip = '10.0.0.1'

ip = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet = IP(dst=server_ip, src=ip) / UDP(dport=53, sport=5530) / DNS(qd=DNSQR(qname='www.google.com', qtype='A', qclass=1))

sock.sendto(raw(packet), (server_ip, 53))

data, address = sock.recvfrom(65000)

data = raw(data)

response = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

print('******* DNS Response for twitter ipv4 address query ***********')

for i in range(response[DNS].ancount) :

	print(response[DNS].an[i].rdata)