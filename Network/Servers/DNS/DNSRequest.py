from scapy.all import *

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet = IP(dst='127.0.0.1') / UDP(dport=53) / DNS(id=12, qd=DNSQR(qname='youtube.com', qtype='TXT'))

sock.sendto(raw(packet), ('127.0.0.1', 53))

data, address = sock.recvfrom(512)

data = raw(data)

response = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

print(len(response) / len(packet))

if response.haslayer(DNS) :

	for i in range(response[DNS].ancount) :

		print(response[DNS].an[i].rdata)