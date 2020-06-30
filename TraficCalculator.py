"""
	class for calculating each flow attr
"""

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
		generate flow id
		@param {Packet} packet
		@return {String}
	"""
	def generate_flow_id (self, flow_match) :

		min_ip = None
		max_ip = None

		min_port = None
		max_port = None

		port_src = None
		port_dst = None

		if flow_match['ipv4_src'] < flow_match['ipv4_dst'] :

			min_ip = flow_match['ipv4_src']
			max_ip = flow_match['ipv4_dst']

		else :

			min_ip = flow_match['ipv4_dst']
			max_ip = flow_match['ipv4_src']

		if flow_match['ip_proto'] == self.ip_protocol_codes['TCP'] :

			port_src = flow_match['tcp_src']
			port_dst = flow_match['tcp_dst']

		elif flow_match['ip_proto'] == self.ip_protocol_codes['UDP'] :

			port_src = flow_match['udp_src']
			port_dst = flow_match['udp_dst']

		if port_src < port_dst :

			min_port = port_src
			max_port = port_dst

		else :

			min_port = port_dst
			max_port = port_src

		return f'{min_ip}-{max_ip}-{min_port}-{max_port}-{flow_match["ip_proto"]}'


	"""
		install flow infos for the first time
		@param {String} flow_id
		@return {Void}
	"""
	def init_flow_infos (self, flow_id) :

		if flow_id not in self.flow_infos :

			self.flow_infos[flow_id] = 1

		else :

			self.flow_infos[flow_id] += 1 

	"""
		fire trafic calculation
		@param {Packet} packet
		@return {String}
	"""
	def calculate (self, packet, flow_match) :

		if flow_match['ip_proto'] == self.ip_protocol_codes['TCP'] or flow_match['ip_proto'] == self.ip_protocol_codes['UDP'] :

			flow_id = self.generate_flow_id(flow_match)

			self.init_flow_infos(flow_id)

			print('flow_infos', self.flow_infos)