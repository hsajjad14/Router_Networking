#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.2.0.1/24')
        r3 = self.addHost('r3', cls=LinuxRouter, ip='10.3.0.1/24')

        # Add 2 switches
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Add host-switch links in the same subnet
        self.addLink(s3,
                     r2,
                     intfName2='r2-eth0',
                     params2={'ip': '10.2.0.1/24'})

        self.addLink(s4,
                     r3,
                     intfName2='r3-eth0',
                     params2={'ip': '10.3.0.1/24'})

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r2,
                     r3,
                     intfName1='r2-eth1',
                     intfName2='r3-eth1',
                     params1={'ip': '10.0.4.1/24'},
                     params2={'ip': '10.0.4.2/24'})

        # Adding hosts specifying the default route
        h6 = self.addHost(name='h6',
                          ip='10.2.0.2/24',
                          defaultRoute='via 10.2.0.1')
        h7 = self.addHost(name='h7',
                          ip='10.3.0.2/24',
                          defaultRoute='via 10.3.0.1')

        # Add host-switch links
        self.addLink(h6, s3)
        self.addLink(h7, s4)


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.0.4.2 dev r2-eth1"))
    info(net['r3'].cmd("ip route add 10.2.0.0/24 via 10.0.4.1 dev r3-eth1"))

    net.start()
    CLI(net)
    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    run()
