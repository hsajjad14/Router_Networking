#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


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


def runOSPF(net):
    all_hosts = net.keys()
    print("ALL HOSTS: ", all_hosts)

    all_routers = []

    for h in all_hosts:
        if h[0] == 'r':
            all_routers.append(h)

    print("ALL ROUTERS: ", all_routers)
    map_of_routers_and_links = {}

    for r1 in all_routers:
        for r2 in all_routers:
            if r1 != r2:
                r1_node = net.getNodeByName(r1)
                r2_node = net.getNodeByName(r2)
                links_between = net.linksBetween(r1_node,r2_node)
                #print(r1, r2)
                # ASSUMING A SINGLE LINK BETWEEN EACH ROUTER!!!
                link_exists = links_between != []  
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
    # since all links cost is the same just use bfs to find shortest paths

    # for each router get shortest path to every other router
    # get the first router in that shortest path

    cached_router_paths = {}
    #path = BFS_SP(map_of_routers_and_links, "r1","r2")
    #print("asdfasdf --- ",path)

    for r1 in all_routers:
        for r2 in all_routers:
            if r1 != r2:
                if (r1, r2) not in cached_router_paths and (r1, r2) not in cached_router_paths:
                    cached_router_paths[(r1, r2)] = BFS_SP(map_of_routers_and_links, r1, r2)
                    cached_router_paths[(r2, r1)] = list(reversed(cached_router_paths[(r1, r2)]))

    print(cached_router_paths)

    # set routing tables
    for router in all_routers:
        router_node = net.getNodeByName(router)
        interfaces = router_node.intfNames()
        print("router " + router + ": interface: " + str(interfaces))
        for interface in interfaces:
            print("AAAAAAAAAAA",interface)
            if router_node.MAC(interface):
                print("\tMAC:", router_node.MAC(interface))
            if router_node.IP(interface):
                print("\t IP:", router_node.IP(interface))
            #print("\t ip of "+interface+" = " + router_node.IP(interface))
        #print("\t of " + interfaces[0] + ":: ip =" + router_node.IP(interfaces[0]))

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

    print("switches under router: ", switches_under_router)
    
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
                            print("\t\tip:", host_node.IP(i))


    print("hosts under switches: ", hosts_under_switches)
    
    hosts_under_routers = {}
    for k,v in switches_under_router.items():
        hosts_under_routers[k] = []
        for s in v:
            hosts_under_routers[k] += hosts_under_switches[s]

    print("hosts under routers: ", hosts_under_routers)

    for k,v in cached_router_paths.items():
        print(k)
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
            #print("wtf", list_host_ip, hosts_ips[host])
            adjusted_ip = ".".join(list_host_ip) + ".0"
            if adjusted_ip not in subnet_hosts:
                #print("adjusted ip = ", adjusted_ip)
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

def get_hosts_under_switches():
    pass

def get_switches_under_routers():
    pass

def get_hosts_under_routers():
    pass


def find_interfaces_on_same_subnet(router1, router2):
    interfaces_router1 = router1.intfNames()
    interfaces_router2 = router2.intfNames()

    for interface_on_r1 in interfaces_router1:
        for interface_on_r2 in interfaces_router2:
            r1_ip = router1.IP(interface_on_r1)
            r2_ip = router2.IP(interface_on_r2)
            #print(interface_on_r1, interface_on_r2)
            if interface_on_r1[-1] != '0' and interface_on_r2[-1] != '0' and r1_ip and r2_ip:
                #print("RRRRRRRRRRR----\t",r1_ip.split("."), r2_ip.split("."))
                if r1_ip.split(".")[:3] == r2_ip.split(".")[:3]:
                    #pass
                    return (interface_on_r1, r1_ip, r2_ip)

    return None
                




def BFS_SP(graph, start, goal):
    explored = []
     
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]
     
    # If the desired node is
    # reached
    if start == goal:
        print("Same Node")
        return
     
    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]
         
        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]
             
            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                 
                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)
 
    # Condition when the nodes
    # are not connected
    print("So sorry, but a connecting"\
                "path doesn't exist :(")
    return
    

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    #info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.0.4.2 dev r2-eth1"))
    #info(net['r3'].cmd("ip route add 10.2.0.0/24 via 10.0.4.1 dev r3-eth1"))
    
    net['r1'].cmd("./scripts_for_router1.sh")
    net['r2'].cmd("./scripts_for_router2.sh")
    net['r3'].cmd("./scripts_for_router3.sh")
    net['r4'].cmd("./scripts_for_router4.sh")

    net.start()
    print("==========NETWORK START==========")
    
    
    runOSPF(net)

    CLI(net)

    #runOSPF(net)

    print("==========CLI - NET START==========")
    net.stop()
    print("==========NETWORK END==========")




if __name__ == '__main__':
    setLogLevel('info')
    run()
