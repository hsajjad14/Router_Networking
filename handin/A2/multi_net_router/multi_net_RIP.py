#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

import os
import time

class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
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


def bellmanFord(graph, all_routers, src):
    # Note: Bellman-Ford's algorithm is used to compute single-source shortest path
    # for weighted graphs. Particularly usefule for when a graph has a negative edge
    # or negative weight cycle.
    # The topology used has uniform link weights of 1 since hop count is used to measure cost.

    distances = {vertex: float("Inf") for vertex in all_routers}
    distances[src] = 0
    predecessors = {vertex: None for vertex in all_routers}
    num_vertices = len(all_routers)

    # relax the edges num_vertices - 1 times
    for i in range(num_vertices - 1):
        for r in graph:
            for r_neighbour in graph[r]:
                if distances[r] != float("Inf") and distances[r] + 1 < distances[r_neighbour]:
                    distances[r_neighbour], predecessors[r_neighbour] = distances[r] + 1, r

    # detect any negative cycles
    # note: in practice for this example, not be needed since all weights on the graph will be 1 (non-negative)
    for r in graph:
        for r_neighbour in graph[r]:
            assert distances[r_neighbour] <= distances[r] + 1, "Error: negative weight cycle"

    # recover the shortest paths based on predecessors dictionary
    shortest_paths = {(src, vertex): [] for vertex in predecessors}
    for r in predecessors:
        if distances[r] > 15:
            continue
        if r != src:
            curr = predecessors[r]
            if curr == None:
                continue
            # push the destination <r> and its predecessor into the path list
            shortest_paths[(src, r)].insert(0, r)
            shortest_paths[(src, r)].insert(0, curr)
            while(curr != src):
                curr = predecessors[curr]
                shortest_paths[(src, r)].insert(0, curr)

    return shortest_paths

   
def runBellmanFord(map_of_routers_and_links, all_routers):
    router_paths = {}

    for r in all_routers:
        path_set = bellmanFord(map_of_routers_and_links, all_routers, r)
        for src_dst_tup in path_set:
            router_paths[src_dst_tup] = path_set[src_dst_tup]
    return router_paths

def runRIP(net):
    all_hosts = net.keys()
    print("ALL HOSTS: ", all_hosts)

    # get all the routers in the network
    all_routers = []
    for h in all_hosts:
        if h[0] == 'r':
            all_routers.append(h)
    print("ALL ROUTERS: ", all_routers)

    # construct the graph of the network
    map_of_routers_and_links = {}

    for r1 in all_routers:
        for r2 in all_routers:
            if r1 != r2:
                r1_node = net.getNodeByName(r1)
                r2_node = net.getNodeByName(r2)
                links_between = net.linksBetween(r1_node,r2_node)
                # ASSUMING A SINGLE LINK BETWEEN EACH ROUTER!!!
                link_exists = (links_between != [])  
                if link_exists and r1 not in map_of_routers_and_links:
                    map_of_routers_and_links[r1] = [r2]
                elif link_exists and r1 in map_of_routers_and_links and r2 not in map_of_routers_and_links[r1]:
                    map_of_routers_and_links[r1].append(r2)

                if link_exists and r2 not in map_of_routers_and_links:
                    map_of_routers_and_links[r2] = [r1]
                elif link_exists and r2 in map_of_routers_and_links and r1 not in map_of_routers_and_links[r2]:
                    map_of_routers_and_links[r2].append(r1)
                    
    print("map of routers and links: ", map_of_routers_and_links)

    # assume all links have uniform cost of 1
    # for each router get shortest path to every other router
    # get the first router in that shortest path

    cached_router_paths = runBellmanFord(map_of_routers_and_links, all_routers)
    print(cached_router_paths)

    # set routing tables

    switches_under_router = get_switches_under_routers(net, all_hosts, all_routers)
    print("switches under router: ", switches_under_router)

    hosts_under_switches, hosts_ips = get_hosts_under_switches(net, all_hosts)
    print("hosts under switches: ", hosts_under_switches)
    
    hosts_under_routers = get_hosts_under_routers(switches_under_router, hosts_under_switches)
    print("hosts under routers: ", hosts_under_routers)

    for k,v in cached_router_paths.items():
        if len(v) < 2:
            # i.e. no path found from source to destination
            continue
        r_s = k[0]
        r_d = k[1]
        r_after_s = v[1]

        router_source = net.getNodeByName(r_s)
        router_destination = net.getNodeByName(r_d)
        
        first_router_after_source = net.getNodeByName(r_after_s)
        interfaces_on_first_router = first_router_after_source.intfNames()
        interfaces_on_source_router = router_source.intfNames()

        # find interfaces on the same subnet
        ips = find_interfaces_on_same_subnet(router_source, first_router_after_source)
        if ips == None:
            continue

        interface_on_source, ip_source_router, ip_first_router = ips
        print("\t\t\t--- ips: ",ip_source_router, ip_first_router)

        hosts_under_destination = hosts_under_routers[r_d]

        # add to ip_source_router routing table to route hosts_under_first_router ips to ip_first_router

        print("\t\t\t-- hosts under destination = ", hosts_under_destination)
        subnet_hosts = []
        for host in hosts_under_destination:
            list_host_ip = hosts_ips[host].split(".")[:3]
            adjusted_ip = ".".join(list_host_ip) + ".0"
            if adjusted_ip not in subnet_hosts:
                subnet_hosts.append(adjusted_ip)
        
        print("subnet hosts = " , subnet_hosts)

        # for every ip in subnet_hosts add /24 to the end then do
        # ip route add 10.2.0.0/24 via 10.0.6.2 dev r1-eth2
        # ip route add subnet_hosts[i]/24 via ip_first_router dev interface_on_source
        print("command: ",r_s, r_d, subnet_hosts, ip_first_router ,interface_on_source )
        
        for sub_host in subnet_hosts:
            add_dash_24_to_ip = sub_host+"/24"
            command = "ip route add "+ add_dash_24_to_ip +" via " + ip_first_router +" dev " + interface_on_source
            print("command to send!!! : ", command)
            net[r_s].cmd(command)

    print("=======ROUTING TABLES=======")
    for r in all_routers:
        net[r].cmdPrint("route")
    print("=======ROUTING TABLES=======")

def get_hosts_under_switches(net, all_hosts):
    hosts_under_switches = {}
    hosts_ips = {}
    for h in all_hosts:
        for s in all_hosts:
            if s[0] == 's' and s not in hosts_under_switches:
                hosts_under_switches[s] = []

            if s[0] == 's' and h[0] == 'h':
                # it is a switch
                # check if it links to the router
                # if it does add it to the map
                host_node = net.getNodeByName(h)
                switch_node = net.getNodeByName(s)
                links_between = net.linksBetween(host_node, switch_node)
                if links_between != []:
                    hosts_under_switches[s].append(h)
                    host_interfaces = host_node.intfNames()
                    print("host_interfaces: ", h, host_interfaces)

                    for i in host_interfaces:
                        if host_node.IP(i) and h not in hosts_ips:
                            hosts_ips[h] = host_node.IP(i)
                            #print("\t\tip:", host_node.IP(i))

    return hosts_under_switches, hosts_ips

def get_switches_under_routers(net, all_hosts, all_routers):
    switches_under_router = {}
    for h in all_hosts:
        for r in all_routers:
            if r not in switches_under_router:
                switches_under_router[r] = []

            if h[0] == 's':
                # it is a switch
                # check if it links to the router
                # if it does add it to the map
                s = h
                router_node = net.getNodeByName(r)
                switch_node = net.getNodeByName(s)
                links_between = net.linksBetween(router_node, switch_node)
                if links_between != []:
                    switches_under_router[r].append(s)

    return switches_under_router


def get_hosts_under_routers(switches_under_router, hosts_under_switches):
    hosts_under_routers = {}
    for k,v in switches_under_router.items():
        hosts_under_routers[k] = []
        for s in v:
            hosts_under_routers[k] += hosts_under_switches[s]

    return hosts_under_routers


def find_interfaces_on_same_subnet(router1, router2):
    interfaces_router1 = router1.intfNames()
    interfaces_router2 = router2.intfNames()

    for interface_on_r1 in interfaces_router1:
        for interface_on_r2 in interfaces_router2:
            r1_ip = router1.IP(interface_on_r1)
            r2_ip = router2.IP(interface_on_r2)
            if interface_on_r1[-1] != '0' and interface_on_r2[-1] != '0' and r1_ip and r2_ip:
                if r1_ip.split(".")[:3] == r2_ip.split(".")[:3]:
                    #pass
                    return (interface_on_r1, r1_ip, r2_ip)

    return None

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # info(net['r1'].cmd("./scripts_for_router1.sh"))
    # info(net['r2'].cmd("./scripts_for_router2.sh"))
    # info(net['r3'].cmd("./scripts_for_router3.sh"))
    # info(net['r4'].cmd("./scripts_for_router4.sh"))
    net['r1'].cmd("./scripts_for_router1.sh")
    net['r2'].cmd("./scripts_for_router2.sh")
    net['r3'].cmd("./scripts_for_router3.sh")
    net['r4'].cmd("./scripts_for_router4.sh")

    net.start()
    print("==========NETWORK START==========")

    pid = os.fork()

    print("+++++++ROUTING TABLES BEFORE RIP+++++++")
    net['r1'].cmdPrint("route")
    net['r2'].cmdPrint("route")
    net['r3'].cmdPrint("route")
    net['r4'].cmdPrint("route")
    print("+++++++ROUTING TABLES BEFORE RIP+++++++")
    time.sleep(10)
    if pid == 0:
        while(True):
            start = time.time()
            runRIP(net)
            end = time.time()
            full_time = end - start
            print("RIP TIME TAKEN = ", full_time)
            time.sleep(30)

    CLI(net)
    print("==========CLI - NET START==========")
        
    net.stop()
    print("==========NETWORK END==========")


if __name__ == '__main__':
    setLogLevel('info')
    run()
