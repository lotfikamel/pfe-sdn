"""
	class for calculating each flow attr
"""

from scapy.all import *

from datetime import datetime, timedelta

from pprint import pprint

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
			fixed ip header length
		"""
		self.HEADERS_LEN = {

			'IP' : 20,
			'UDP' : 8,
			'TCP' : 20
		}

	"""
		begin sniffing
		@return {Void}
	"""
	def init_sniff (self) :

		sniff(lfilter=self.filter_packet, prn=self.on_packet)

	"""
		filter packet to sniff
		@param {Packet} packet
		@retrun {Boolean}
	"""
	def filter_packet (self, packet) :

		return (IP in packet) and ( (TCP in packet) or (UDP in packet) )

	"""
		on packet sniffed
		@param {Packet} packet
		@return {Void}
	"""
	def on_packet (self, packet) :

		print(self.get_packet_net_payload_len(packet))

		flow_id = self.generate_flow_id(packet)

		if flow_id in self.flow_infos :

			self.calculate(flow_id, packet)

		# fist packet in the flow
		else :

			self.init_flow(flow_id, packet)

		pprint(self.flow_infos)

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

			'packet_per_second' : 0,

			'bytes_per_second' : 0,

			'forward' : {

				'total' : 1,
				'total_length' : self.get_packet_net_payload_len(packet),
				'total_header_length' : self.get_protocol_header_length(packet)
			},

			'backward' : {

				'total' : 0,
				'total_length' : 0,
				'total_header_length' : 0
			}
		}

	""" 
		Determine if the flow diretion is forward
		@param {String} flow_id
		@param {Packet} packet
		@return {Boolean}
	"""
	def is_forward  (self, flow_id, packet) :

		return packet[IP].src == self.flow_infos[flow_id]['ip_forwarded']

	"""
		get protocol constant length
		@param {Packet} packet
		@return {Integer}
	"""
	def get_protocol_header_length (self, packet) :

		if TCP in packet :

			protocol_header_length = self.HEADERS_LEN['TCP']

		elif UDP in packet :

			protocol_header_length = self.HEADERS_LEN['UDP']

		return protocol_header_length

	"""
		get packet net payload length
		@param {Packet} packet
		@return {Integer}
	"""
	def get_packet_net_payload_len (self, packet) :

		if TCP in packet :

			protocol_header_length = self.HEADERS_LEN['TCP']

		elif UDP in packet :

			protocol_header_length = self.HEADERS_LEN['UDP']

		return packet[IP].len - self.HEADERS_LEN['IP'] - protocol_header_length

	"""
		fire trafic calculation
		@param {Packet} packet
		@return {Void}
	"""
	def calculate (self, flow_id, packet) :

		self.calculate_flow_duration(flow_id, packet)

		#call all forward functions
		if self.is_forward(flow_id, packet) :

			self.calculate_total_forwarded_packets(flow_id, packet)

			self.calculate_total_forwarded_packets_length(flow_id, packet)

			self.calculate_total_forwarded_header_length(flow_id, packet)

		#call all backward functions
		else :

			self.calculate_total_backwards_packets(flow_id, packet)

			self.calculate_total_backward_packets_length(flow_id, packet)

			self.calculate_total_backward_header_length(flow_id, packet)

		self.calculate_flow_packets_per_second(flow_id)

		self.calculate_flow_bytes_per_second(flow_id)

	"""
		calculate flow duration
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_flow_duration (self, flow_id, packet) :

		diff = datetime.now() - self.flow_infos[flow_id]['first_packet_time']

		duration_microseconds = diff / timedelta(microseconds=1)

		self.flow_infos[flow_id]['duration'] = duration_microseconds

	"""
		calculate total forwarded packets
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_total_forwarded_packets (self, flow_id, packet) :

		self.flow_infos[flow_id]['forward']['total'] += 1

	"""
		calculate total backward packets
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_total_backwards_packets (self, flow_id, packet) :

		self.flow_infos[flow_id]['backward']['total'] += 1

	"""
		calculate total forward packets length
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_total_forwarded_packets_length (self, flow_id, packet) :

		self.flow_infos[flow_id]['forward']['total_length'] += self.get_packet_net_payload_len(packet)

	"""
		calculate total backward packets length
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_total_backward_packets_length (self, flow_id, packet) :

		self.flow_infos[flow_id]['backward']['total_length'] += self.get_packet_net_payload_len(packet)

	"""
		calculate forward total header length
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_total_forwarded_header_length (self, flow_id, packet) :

		if TCP in packet :

			protocol_header_length = self.HEADERS_LEN['TCP']

		elif UDP in packet :

			protocol_header_length = self.HEADERS_LEN['UDP']

		self.flow_infos[flow_id]['forward']['total_header_length'] += self.get_protocol_header_length(packet)

	"""
		calculate forward total header length
		@param {String} fow_id
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_total_backward_header_length (self, flow_id, packet) :

		if TCP in packet :

			protocol_header_length = self.HEADERS_LEN['TCP']

		elif UDP in packet :

			protocol_header_length = self.HEADERS_LEN['UDP']

		self.flow_infos[flow_id]['backward']['total_header_length'] += self.get_protocol_header_length(packet)

	"""
		calculate flow packets per second
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_flow_packets_per_second (self, flow_id) :

		total_forwarded_packets = self.flow_infos[flow_id]['forward']['total']

		total_backward_packets = self.flow_infos[flow_id]['backward']['total']

		flow_duration = self.flow_infos[flow_id]['duration'] / 10**6

		self.flow_infos[flow_id]['packet_per_second'] = ( total_forwarded_packets + total_backward_packets ) / flow_duration

	"""
		calculate flow bytes per second
		@param {Packet} packet
		@parm {Void}
	"""
	def calculate_flow_bytes_per_second (self, flow_id) :

		total_forwarded_length = self.flow_infos[flow_id]['forward']['total_length']

		total_backward_length = self.flow_infos[flow_id]['backward']['total_length']

		flow_duration = self.flow_infos[flow_id]['duration'] / 10**6

		self.flow_infos[flow_id]['bytes_per_second'] = ( total_forwarded_length + total_backward_length ) / flow_duration

traficCalculator = TraficCalculator()

traficCalculator.init_sniff()