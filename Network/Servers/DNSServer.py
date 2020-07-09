from scapy.all import *

import socket

from dnslib import DNSRecord

DNS_SERVER_IP = '10.0.0.2'

DNS_SERVER_PORT = 53

local_ip = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

sock.bind((DNS_SERVER_IP, DNS_SERVER_PORT))

while True:

	data, address = sock.recvfrom(512)

	data = raw(data)

	packet = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

	if packet.haslayer(DNSQR) :

		print(packet[UDP].dport)

		packet[DNSQR].show()

exit(0)

BPF_FILTER = f'udp port 53 and ip dst {DNS_SERVER_IP}'

def filter (packet) :

	print(packet.haslayer(DNS))

	return (IP in packet) and (UDP in packet and DNS in packet)

def forward_dns(orig_pkt) :

	pass

	# print(f"Forwarding: {orig_pkt[DNSQR].qname}")

	# packet = IP(dst='8.8.8.8') / UDP(sport=orig_pkt[UDP].sport) / DNS(rd=1, id=orig_pkt[DNS].id, qd=DNSQR(qname=orig_pkt[DNSQR].qname))

	# response = sr1(packet, verbose=0)

	# resp_pkt = IP(dst=orig_pkt[IP].src, src=DNS_SERVER_IP)/UDP(dport=orig_pkt[UDP].sport)/DNS()

	# resp_pkt[DNS] = response[DNS]

	# send(resp_pkt, verbose=0)

	# return f"Responding to {orig_pkt[IP].src}"

def get_response(pkt):

	print(pkt.show())

	if (
		DNS in pkt and
		pkt[DNS].opcode == 0 and
		pkt[DNS].ancount == 0
	) :
		if "trailers.apple.com" in str(pkt["DNS Question Record"].qname) :

			spf_resp = IP(dst=pkt[IP].src) / UDP(dport=pkt[UDP].sport, sport=53) / DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname, rdata=local_ip)/DNSRR(rrname="trailers.apple.com",rdata=local_ip))

			send(spf_resp, verbose=0, iface=IFACE)

			return f"Spoofed DNS Response Sent: {pkt[IP].src}"

		else:
			# make DNS query, capturing the answer and send the answer
			return forward_dns(pkt)

sniff(lfilter=filter, prn=get_response, iface="lo")

