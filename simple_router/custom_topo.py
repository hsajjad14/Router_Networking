"""
Inspired by topo-2sw-2host.py from: http://mininet.org/walkthrough/
Custom mininet topology based on Piazza @249

Two switches, each with its own two hosts and one host that is connected to both switches (the "router")

subnet 10.0.1.1/24, r0-eth1 ip: 10.0.1.1
subnet 10.0.2.1/24, r0-eth2 ip: 10.0.2.1

        router
r1-eth1/     \r1-eth2
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
            r1_eth1 = '10.0.1.1/24'
            r1_eth2 = '10.0.2.1/24'
            r1_eth3 = '10.0.3.1/24'

	    # add hosts and switches
            left_host_s1 = self.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
            right_host_s1 = self.addHost('h3', ip='10.0.1.20/24', defaultRoute='via 10.0.1.1')
            left_host_s2 = self.addHost('h2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')
            right_host_s2 = self.addHost('h4', ip='10.0.2.20/24', defaultRoute='via 10.0.2.1')
            left_host_s3 = self.addHost('h5', ip='10.0.3.10/24', defaultRoute='via 10.0.3.1')
            right_host_s3 = self.addHost('h6', ip='10.0.3.20/24', defaultRoute='via 10.0.3.1')
            router = self.addHost('r1')
            s1 = self.addSwitch('s1')
            s2 = self.addSwitch('s2')
            s3 = self.addSwitch('s3')

	    # add links
            self.addLink(left_host_s1, s1)
            self.addLink(right_host_s1, s1)
            self.addLink(right_host_s2, s2)
            self.addLink(left_host_s2, s2)
            self.addLink(right_host_s3, s3)
            self.addLink(left_host_s3, s3)
            self.addLink(s1, router, intfName2='r1-eth1', params2={ 'ip' : r1_eth1 } )
            self.addLink(s2, router, intfName2='r1-eth2', params2={ 'ip' : r1_eth2 } )
            self.addLink(s3, router, intfName2='r1-eth3', params2={ 'ip' : r1_eth3 } )

            '''
            def addEndSysHost(self, ip_addr):
            new_host = self.addHost('h'+str(self.num_hosts), ip=(ip_addr+'/24'), defaultRoute=('via '+ ip_addr))
            self.addLink(new_host, )
            self.count += 1
            '''

topos = { 'mytopo': ( lambda: MyTopo() ) }
