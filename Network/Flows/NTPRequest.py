from scapy.all import *

import socket

import sys

server_ip = '10.0.0.3'

ip = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet = IP(dst=server_ip, src=ip) / UDP(dport=123,sport=50000) / NTPHeader("\x1b\x00\x00\x00"+"\x00"*11*4)

sock.sendto(raw(packet), (server_ip, 123))

data, address = sock.recvfrom(65000)

data = raw(data)

response = IP(_pkt=data) / UDP(_pkt=data) / NTPHeader(_pkt=data)

print('******* NTP Response ***********')

response[NTPHeader].show()