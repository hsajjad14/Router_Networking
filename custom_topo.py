"""
Inspired by topo-2sw-2host.py from: http://mininet.org/walkthrough/
Custom mininet topology based on Piazza @249

Two switches, each with its own two hosts and one host that is connected to both switches (the "router")

        router
	/     \
   switch    switch
    / \        / \
 host host  host host

Adding the 'topos' dict with a key/value pair to generate the newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

From CLI, run: sudo mn --custom `path to custom_topo.py` --topo mytopo --test pingall
(the pingall is not necessary; just to test)
"""
from mininet.topo import Topo

class MyTopo (Topo):

	def build(self):
		# add hosts and switches
		left_host_s1 = self.addHost('h1')
		right_host_s1 = self.addHost('h3')
		left_host_s2 = self.addHost('h2')
		right_host_s2 = self.addHost('h4')
		router_host = self.addHost('r1')
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')

		# add links
		self.addLink(left_host_s1, s1)
		self.addLink(right_host_s1, s1)
		self.addLink(router_host, s1)
		self.addLink(router_host, s2)
		self.addLink(right_host_s2, s2)
		self.addLink(left_host_s2, s2)

topos = { 'mytopo': ( lambda: MyTopo() ) }
