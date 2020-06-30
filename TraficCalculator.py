"""
	class for calculating each flow attr
"""

from scapy.all import *

from datetime import datetime, timedelta

class TraficCalculator () :

	"""
		init the trafic calculator
	"""
	def __init__ (self) :

		"""
			flow infos data structure
			@var {Dict}
		"""
		self.flow_infos = {}

		"""
			ip protocol with their code
			@var {Dict}
		"""
		self.ip_protocol_codes = {

			'TCP' : 6,
			'UDP' : 17
		}

	"""
		begin sniffing
	"""
	def init_sniff (self) :

		sniff(lfilter=self.filter_packet, prn=self.on_packet)

	"""
		filter packet to sniff
	"""
	def filter_packet (self, packet) :

		return (TCP in packet) or (UDP in packet)

	"""
		packet sniff callback
	"""
	def on_packet (self, packet) :

		print(packet[IP].proto)

		flow_id = self.generate_flow_id(packet)

		if flow_id in self.flow_infos :

			self.calculate(flow_id, packet)

		# fist packet in the flow
		else :

			self.init_flow(flow_id, packet)

		print(self.flow_infos)

		return

	"""
		generate flow id
		@param {Packet} packet
		@return {String}
	"""
	def generate_flow_id (self, packet) :

		min_ip = None
		max_ip = None

		min_port = None
		max_port = None

		port_src = None
		port_dst = None

		if packet[IP].src < packet[IP].dst :

			min_ip = packet[IP].src
			max_ip = packet[IP].dst

		else :

			min_ip = packet[IP].dst
			max_ip = packet[IP].src

		if packet[IP].proto == self.ip_protocol_codes['TCP'] :

			port_src = packet[TCP].sport
			port_dst = packet[TCP].dport

		elif packet[IP].proto == self.ip_protocol_codes['UDP'] :

			port_src = packet[UDP].sport
			port_dst = packet[UDP].dport

		if port_src < port_dst :

			min_port = port_src
			max_port = port_dst

		else :

			min_port = port_dst
			max_port = port_src

		return f'{min_ip}-{max_ip}-{min_port}-{max_port}-{packet[IP].proto}'


	"""
		install flow infos for the first time
		@param {String} flow_id
		@param {Packet} packet
		@return {Void}
	"""
	def init_flow (self, flow_id, packet) :

		self.flow_infos[flow_id] = {

			'protocol' : packet[IP].proto,

			'ip_forwarded' : packet[IP].src,

			'first_packet_time' : datetime.now(),

			'duration' : 0,

			'forward' : {

				'total' : 0
			},

			'backward' : {

				'total' : 0
			}
		}

	"""
		fire trafic calculation
		@param {Packet} packet
		@return {String}
	"""
	def calculate (self, flow_id, packet) :

		self.calculate_flow_duration(flow_id, packet)

	"""
		calculate flow duration
	"""
	def calculate_flow_duration (self, flow_id, packet) :

		diff = datetime.now() - self.flow_infos[flow_id]['first_packet_time']

		duration_microseconds = diff / timedelta(microseconds=1)

		self.flow_infos[flow_id]['duration'] = duration_microseconds

traficCalculator = TraficCalculator()

traficCalculator.init_sniff()