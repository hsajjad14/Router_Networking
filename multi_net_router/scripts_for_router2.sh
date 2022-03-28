#!/bin/bash

echo "Setting up Router"
ifconfig r2-eth0 0
ifconfig r2-eth1 0
ifconfig r2-eth2 0

ifconfig r2-eth0 hw ether 00:00:00:00:02:01
ifconfig r2-eth1 hw ether 00:00:00:00:02:02
ifconfig r2-eth2 hw ether 00:00:00:00:02:03

ip addr add 10.2.0.1/24 brd + dev r2-eth0
ip addr add 10.0.4.1/24 brd + dev r2-eth1
ip addr add 10.0.6.2/24 brd + dev r2-eth2


echo 1 > /proc/sys/net/ipv4/ip_forward

# adding ip route forwarding
ip route add 10.0.1.0/24 via 10.0.6.1 dev r2-eth2
ip route add 10.0.2.0/24 via 10.0.6.1 dev r2-eth2
ip route add 10.3.0.0/24 via 10.0.4.2 dev r2-eth1
ip route add 10.4.0.0/24 via 10.0.4.2 dev r2-eth1

