"""
Inspired by topo-2sw-2host.py from: http://mininet.org/walkthrough/

also: http://csie.nqu.edu.tw/smallko/sdn/mininet_simple_router.html

Simple Router: two switches, each with its own two hosts and one host that is connected to both switches (the "router")

Two simple router's router2 and router1 each conncted to a interface on the monitor node

router topology:
https://piazza.com/class/kxhl6o1cccn2oo?cid=315

subnet 10.0.1.1/24, r1-eth0 ip: 10.0.1.1
subnet 10.0.2.1/24, r1-eth1 ip: 10.0.2.1


Adding the 'topos' dict with a key/value pair to generate the newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

From CLI, run: sudo mn --custom `path to custom_topo.py` --topo mytopo --test pingall
(don't have to include the pingall; can replace with another test or exclude altogether)
"""


from mininet.topo import Topo

class MyTopo (Topo):

        def build(self):

            # router 1
            r1_eth0 = '10.0.1.1/24'
            r1_eth1 = '10.0.2.1/24'
            r1_eth2 = '10.0.6.1/24'
            r1_eth3 = ''

            # add hosts and switches
            h1 = self.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1', mac="00:00:00:00:00:01")
            h3 = self.addHost('h3', ip='10.0.1.20/24', defaultRoute='via 10.0.1.1', mac="00:00:00:00:00:03")
            h2 = self.addHost('h2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1', mac="00:00:00:00:00:02" )
            h4 = self.addHost('h4', ip='10.0.2.20/24', defaultRoute='via 10.0.2.1', mac="00:00:00:00:00:04")
            r1 = self.addHost('r1')
            s1 = self.addSwitch('s1')
            s2 = self.addSwitch('s2')
            
            # add links
            self.addLink(h1, s1)
            self.addLink(h3, s1)
            self.addLink(h2, s2)
            self.addLink(h4, s2)
            self.addLink(r1, s1)
            self.addLink(r1, s2)

            # router 2
            r2_eth0 = '10.2.0.1/24'
            r2_eth1 = '10.0.4.1/24'
            r2_eth2 = '10.0.6.2/24'
            r2_eth3 = ''

            r2 = self.addHost('r2')

            s3 = self.addSwitch('s3')
            h5 = self.addHost('h5', ip='10.2.0.10/24', defaultRoute='via 10.2.0.1', mac="00:00:00:00:00:05")
            h6 = self.addHost('h6', ip='10.2.0.20/24', defaultRoute='via 10.2.0.1', mac="00:00:00:00:00:06")
            
            self.addLink(h5, s3)
            self.addLink(h6, s3)

            self.addLink(r2, s3)
            
            # connecting the two routers r1 and r2
            self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip': '10.0.6.1/24'}, params2={'ip': '10.0.6.2/24'})

            
            # router 3
            r3_eth0 = '10.3.0.1/24'
            r3_eth1 = '10.0.4.2/24'
            r3_eth2 = '10.0.3.2/24'
            r3_eth3 = '10.0.5.1/24'

            r3 = self.addHost('r3')
            h7 = self.addHost('h7', ip='10.3.0.10/24', defaultRoute='via 10.3.0.1', mac="00:00:00:00:00:07")
            s4 = self.addSwitch('s4')

            self.addLink(h7, s4)
            self.addLink(r3, s4)

            # connecting the two routers r1 and r3
            self.addLink(r1, r3, intfName1='r1-eth3', intfName2='r3-eth2', params1={'ip': '10.0.3.1/24'}, params2={'ip': '10.0.3.2/24'})
            # connecting the two routers r2 and r3
            self.addLink(r2, r3, intfName1='r2-eth1', intfName2='r3-eth1', params1={'ip': '10.0.4.1/24'}, params2={'ip': '10.0.4.2/24'})

            # router 4
            r4_eth0 = '10.4.0.1/24'
            r4_eth1 = '10.0.5.2/24'

            r4 = self.addHost('r4')
            h8 = self.addHost('h8', ip='10.4.0.10/24', defaultRoute='via 10.4.0.1', mac="00:00:00:00:00:08")
            s5 = self.addSwitch('s5')

            self.addLink(h8, s5)
            self.addLink(r4, s5)

            # connecting the two routers r3 and r4
            self.addLink(r3, r4, intfName1='r3-eth3', intfName2='r4-eth1', params1={'ip': '10.0.5.1/24'}, params2={'ip': '10.0.5.2/24'})


topos = { 'mytopo': ( lambda: MyTopo() ) }
