"""
Inspired by topo-2sw-2host.py from: http://mininet.org/walkthrough/
Custom mininet topology based on Piazza @249

also: http://csie.nqu.edu.tw/smallko/sdn/mininet_simple_router.html

Two switches, each with its own two hosts and one host that is connected to both switches (the "router")

subnet 10.0.1.1/24, r0-eth0 ip: 10.0.1.1
subnet 10.0.2.1/24, r0-eth1 ip: 10.0.2.1

        router
r1-eth0/     \r1-eth1
   switch    switch
    / \        / \
 host host  host host


Adding the 'topos' dict with a key/value pair to generate the newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

From CLI, run: sudo mn --custom `path to custom_topo.py` --topo mytopo
"""


from mininet.topo import Topo

class MyTopo (Topo):

        def build(self):
            r1_eth0 = '10.0.1.1/24'
            r1_eth1 = '10.0.2.1/24'

            # add hosts and switches
            left_host_s1 = self.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1', mac="00:00:00:00:00:01")
            right_host_s1 = self.addHost('h3', ip='10.0.1.20/24', defaultRoute='via 10.0.1.1', mac="00:00:00:00:00:03")
            left_host_s2 = self.addHost('h2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1', mac="00:00:00:00:00:02" )
            right_host_s2 = self.addHost('h4', ip='10.0.2.20/24', defaultRoute='via 10.0.2.1', mac="00:00:00:00:00:04")
            router = self.addHost('r1')
            s1 = self.addSwitch('s1')
            s2 = self.addSwitch('s2')

            # add links
            self.addLink(left_host_s1, s1)
            self.addLink(right_host_s1, s1)
            self.addLink(right_host_s2, s2)
            self.addLink(left_host_s2, s2)
            self.addLink(router, s1)
            self.addLink(router, s2)

topos = { 'mytopo': ( lambda: MyTopo() ) }
