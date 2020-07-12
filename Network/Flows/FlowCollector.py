import socket

from TraficCalculator import TraficCalculator

import sys

import pickle

"""
	send all calculated flows via udp socket
"""
class FlowCollector :

	def __init__ (self, ip, port) :

		self.SERVER_PORT = port

		self.SERVER_IP = ip

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.traficCalculator = TraficCalculator()

	def start (self) :

		print(f'Flow Collector Server started and waiting for queries from the SDN controller on {self.SERVER_IP}:{self.SERVER_PORT}...')

		#start calculation thread
		self.traficCalculator.start()

		#bind the socket
		self.sock.bind((self.SERVER_IP, self.SERVER_PORT))

		while True:

			data, address = self.sock.recvfrom(1024)

			event = data.decode('utf-8')

			if event == 'GET_FLOWS' :

				binary_flows = self.traficCalculator.get_flows_as_binary()

				self.sock.sendto(binary_flows, address)

flowCollector = FlowCollector(sys.argv[1], 6000)

flowCollector.start()