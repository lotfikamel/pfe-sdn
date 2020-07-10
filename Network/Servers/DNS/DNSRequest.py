from scapy.all import *

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(0, 2) :

	packet = IP(dst='127.0.0.1') / UDP(dport=53) / DNS(qd=DNSQR(qname='google.com', qtype='TXT'))

	sock.sendto(raw(packet), ('127.0.0.1', 53))

	data, address = sock.recvfrom(512)

	data = raw(data)

	packet = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

	if packet.haslayer(DNSRR) :

		packet[DNSRR].show()