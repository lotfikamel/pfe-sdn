from scapy.all import *

tcp_counts = 0

udp_counts = 0

def filter (packet) :

	return TCP in packet

def packet_sniffer (packet) :

	if TCP in packet :

		global tcp_counts

		tcp_counts += 1

	if UDP in packet :

		global udp_counts

		udp_counts += 1

	print(f'UDP counts {udp_counts} TCP {tcp_counts} IP source {packet[IP].src} IP dst {packet[IP].dst}')

sniff(lfilter=filter, prn=packet_sniffer)