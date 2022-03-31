#!/bin/bash

echo "Setting up Router"
ifconfig r4-eth0 0
ifconfig r4-eth1 0

ifconfig r4-eth0 hw ether 00:00:00:00:04:01
ifconfig r4-eth1 hw ether 00:00:00:00:04:02

ip addr add 10.4.0.1/24 brd + dev r4-eth0
ip addr add 10.0.5.2/24 brd + dev r4-eth1

echo 1 > /proc/sys/net/ipv4/ip_forward

#ip route add 10.0.2.0/24 via 10.0.5.1 dev r4-eth1
#ip route add 10.0.1.0/24 via 10.0.5.1 dev r4-eth1
#ip route add 10.2.0.0/24 via 10.0.5.1 dev r4-eth1
#ip route add 10.3.0.0/24 via 10.0.5.1 dev r4-eth1

