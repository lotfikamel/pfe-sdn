from scapy.all import *

import sys

import socket

import json

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

		self.data = self.load_data()

		self.query_received = 0

	"""
		load dns json data
		@return {Dict}
	"""
	def load_data (self) :

		file = open('./dns_records.json', 'r')

		return json.load(file)

	"""
		parse qname (domain name)
		@param {Packet} packet
		@return {String}
	"""
	def parse_qname (self, packet) :

		qname = packet[DNSQR].qname.decode('utf-8').split('.')[:-1]

		#remove www from the begining
		qname = [chunk for chunk in qname if chunk != 'www']

		qname = str.join('.', qname)

		return qname

	"""
		parse query type field
		@param {Packet} packet
		@return {String}
	"""
	def parse_qtype (self, packet) :

		return str(packet[DNSQR].qtype)

	"""
		check if the record asked exists
		@param {String} qname
		@param {String} qtype
		@return {Boolean}
	"""
	def is_records_exists (self, qname, qtype) :

		return qname in self.data and qtype in self.data[qname]

	"""
		build dns response packet
		@param {Packet} packet
		@param {String} qname
		@param {String} qtype
		@return {Packet}
	"""
	def build_record_response (self, packet, qname, qtype) :

		ip = IP(dst=packet[IP].src, src=self.DNS_SERVER_IP)

		udp =  UDP(dport=packet[UDP].sport, sport=self.DNS_SERVER_PORT)

		qd = DNSQR(qname=packet[DNSQR].qname)

		ancount = len(self.data[qname][qtype])

		an = None

		if ancount > 0 :

			an = DNSRR(

				rrname=packet[DNSQR].qname,
				type=packet[DNSQR].qtype,
				ttl=self.data[qname][qtype][0]['ttl'],
				rclass=self.data[qname][qtype][0]['rclass'],
				rdlen=self.data[qname][qtype][0]['rdlen'],
				rdata=self.data[qname][qtype][0]['rdata']
			)

			if ancount > 1 :

				for i in range(1, ancount) :

					an = an / DNSRR(

						rrname=packet[DNSQR].qname,
						type=packet[DNSQR].qtype,
						ttl=self.data[qname][qtype][i]['ttl'],
						rclass=self.data[qname][qtype][i]['rclass'],
						rdlen=self.data[qname][qtype][i]['rdlen'],
						rdata=self.data[qname][qtype][i]['rdata']
					)

		dns = DNS(id=packet[DNS].id,ancount=ancount,an=an, qd=qd)

		return ip / udp / dns

	"""
		start the server
		@return {Void}
	"""
	def start (self) :

		print(f'DNS Server started and waiting for queries on {self.DNS_SERVER_IP}:{self.DNS_SERVER_PORT}...')

		#bind the socket
		self.sock.bind((self.DNS_SERVER_IP, self.DNS_SERVER_PORT))

		while True:

			print('waiting for queries ...')

			data, address = self.sock.recvfrom(65000)

			self.query_received += 1

			data = raw(data)

			packet = IP(_pkt=data) / UDP(_pkt=data) / DNS(_pkt=data)

			if packet.haslayer(DNSQR) :

				qname = self.parse_qname(packet)

				qtype = self.parse_qtype(packet)

				if self.is_records_exists(qname, qtype) :

					response = self.build_record_response(packet, qname, qtype)

					print(packet[IP].src)

					self.sock.sendto(raw(response), (packet[IP].src, address[1]))

			print('query_received', self.query_received)
			

server_ip = sys.argv[1]

dnsServer = DNSServer(server_ip)

dnsServer.start()