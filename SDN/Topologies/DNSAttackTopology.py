from mininet.topo import Topo

from mininet.net import Mininet

from mininet.link import TCLink

from mininet.log import setLogLevel

from mininet.cli import CLI

from mininet.node import OVSKernelSwitch, RemoteController

from threading import Thread

import socket

import json

class BandwidthTester (Thread) :

	"""
		Init bw tester
		@param {Mininet} net
	"""
	def __init__ (self, net) :

		Thread.__init__(self)

		self.net = net

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.sock.settimeout(5)

		self.kill = False

	def kill_server (self) :

		self.kill = True

		self.sock.close()

	"""
		run the thread
	"""
	def run (self) :

		print('bandwidth tester started and waiting for requests on port 1000 ...')

		self.sock.bind(('127.0.0.1', 1000))

		global RUN_SERVER

		while True and self.kill == False:

			try :

				data, address = self.sock.recvfrom(65000)

				data = data.decode('utf-8')

				data = json.loads(data)

				event = data['event']

				if event == 'TEST_BANDWIDTH' :

					bw = self.net.iperf(hosts=[self.net.get(data['data'][0]), self.net.get(data['data'][1])])

					response = {}

					response['event'] = event

					response['data'] = bw

					self.sock.sendto(bytes(json.dumps(response)), address)

			except Exception as e:

				pass

class DNSAttackTopology (Topo) :

	"""
		build and define topologies host, switches and links
		@retrun {Void}
	"""
	def build (self) :

		#define switch
		switch = self.addSwitch('s1', cls=OVSKernelSwitch)

		#define DNS Servers
		DNS1 = self.addHost('DNS1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
		DNS2 = self.addHost('DNS2', mac='00:00:00:00:00:02', ip='10.0.0.2/8')

		NTP1 = self.addHost('NTP1', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
		NTP2 = self.addHost('NTP2', mac='00:00:00:00:00:04', ip='10.0.0.4/8')

		#define victime and attacker hosts
		victime = self.addHost('victime', mac='00:00:00:00:00:05', ip='10.0.0.5')
		attacker = self.addHost('attacker', mac='00:00:00:00:00:06', ip='10.0.0.6')

		self.addLink(DNS1, switch)
		self.addLink(DNS2, switch)

		self.addLink(NTP1, switch)
		self.addLink(NTP2, switch)

		self.addLink(victime, switch)
		self.addLink(attacker, switch)

def start_network () :

	topo = DNSAttackTopology()

	controller = RemoteController('controller', controller=RemoteController, port=6653)

	net = Mininet(topo=topo, link=TCLink, controller=controller)

	bandwidthTester = BandwidthTester(net)

	bandwidthTester.start()

	net.start()

	net.pingAll()

	CLI(net)

	net.stop()

	bandwidthTester.kill_server()

if __name__ == '__main__' :

	setLogLevel( 'info' )

	start_network()