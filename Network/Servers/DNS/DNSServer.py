from scapy.all import *

import socket

class DNSServer :

	"""
		init the dns server
		@param {String} dns_server_ip
		@return {Void}
	"""
	def __init__ (self, dns_server_ip) :

		self.DNS_SERVER_IP = dns_server_ip

		self.DNS_SERVER_PORT = 53

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	"""
		start the server
		@return {Void}
	"""
	def start (self) :

		#bind the socket
		self.sock.bind((self.DNS_SERVER_IP, self.DNS_SERVER_PORT))

		while True:

			data, address = self.sock.recvfrom(512)

			data = raw(data)

			packet = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

			if packet.haslayer(DNSQR) :

				print(packet[UDP].len)

				google = IP(dst='8.8.8.8') / UDP(sport=packet[UDP].sport) / DNS(rd=1, id=packet[DNS].id, qd=DNSQR(qname=packet[DNSQR].qname, qtype=packet[DNSQR].qtype))

				response = sr1(google, verbose=False)

				response.show()

				print(response[UDP].len / packet[UDP].len)
				
				ip = IP(dst='127.0.0.1', src='127.0.0.1')

				udp =  UDP(dport=packet[UDP].sport, sport=53)

				dns = DNS(id=packet[DNS].id,ancount=1,an=DNSRR(rrname=packet[DNSQR].qname, type=packet[DNSQR].qtype, rdata='12.12.12.12'), qd=DNSQR(qname=packet[DNSQR].qname))

				spf_resp = ip / udp / dns

				self.sock.sendto(raw(spf_resp), address)

dnsServer = DNSServer('127.0.0.1')

dnsServer.start()