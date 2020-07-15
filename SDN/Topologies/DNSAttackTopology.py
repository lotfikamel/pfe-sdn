from mininet.topo import Topo

from mininet.net import Mininet

from mininet.link import TCLink

from mininet.log import setLogLevel

from mininet.cli import CLI

from mininet.node import OVSKernelSwitch, RemoteController

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

		#define victime and attacker hosts
		victime = self.addHost('victime', mac='00:00:00:00:00:03', ip='10.0.0.3')
		attacker = self.addHost('attacker', mac='00:00:00:00:00:04', ip='10.0.0.4')

		self.addLink(DNS1, switch)
		self.addLink(DNS2, switch)

		self.addLink(victime, switch)
		self.addLink(attacker, switch)

def start_network () :

	topo = DNSAttackTopology()

	controller = RemoteController('controller', controller=RemoteController, port=6653)

	net = Mininet(topo=topo, link=TCLink, controller=controller)

	net.start()

	net.startTerms()

	CLI(net)

	net.stop()

if __name__ == '__main__' :

	setLogLevel( 'info' )

	start_network()