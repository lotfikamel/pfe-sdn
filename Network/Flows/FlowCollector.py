import socket

from TraficCalculator import TraficCalculator

import pickle

import json

"""
	send all calculated flows via udp socket
"""
class FlowCollector :

	def __init__ (self, ip, port) :

		self.SERVER_PORT = port

		self.SERVER_IP = ip

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.traficCalculator = TraficCalculator()

		self.final_predictions = {}

		self.topology = {}

	def start (self) :

		print(f'Flow Collector Server started and waiting for queries from the SDN controller on {self.SERVER_IP}:{self.SERVER_PORT}...')

		#start calculation thread
		self.traficCalculator.start()

		#bind the socket
		self.sock.bind((self.SERVER_IP, self.SERVER_PORT))

		while True:

			data, address = self.sock.recvfrom(65000)

			data = data.decode('utf-8')

			data = json.loads(data)

			print(data['event'])

			if data['event'] == 'GET_FLOWS' :

				binary_flows, json_flow = self.traficCalculator.get_flows_as_binary()

				self.sock.sendto(binary_flows, address)

			if data['event'] == 'GET_FLOWS_MONITOR' :

				binary_flows, flow_monitor = self.traficCalculator.get_flows_as_binary()

				monitor = {}

				monitor['event'] = data['event']

				monitor['data'] = flow_monitor

				self.sock.sendto(bytes(json.dumps(monitor), 'utf-8'), address)

			if data['event'] == 'FINAL_PREDICTION' :

				for i in data['data'] :

					self.final_predictions[i] = data['data'][i]

				print(self.final_predictions)

			if data['event'] == 'GET_FINAL_PREDICTION' :

				final = {}

				final['event'] = data['event']

				final['data'] = {}

				for flow_id in self.final_predictions :

					final['data'][flow_id] = { 'prediction' : self.final_predictions[flow_id] }

					final['data'][flow_id].update({ 'ips' : self.traficCalculator.get_flow_ips(flow_id) })

				self.sock.sendto(bytes(json.dumps(final), 'utf-8'), address)

			if data['event'] == 'UPDATE_TOPOLOGY' :

				print('topology', data['data'])

				self.topology = data['data']

flowCollector = FlowCollector('127.0.0.1', 6000)

flowCollector.start()