#!/bin/bash


echo "Setting up Router"
ifconfig r3-eth0 0
ifconfig r3-eth1 0

ifconfig r3-eth0 hw ether 00:00:00:00:03:01
ifconfig r3-eth1 hw ether 00:00:00:00:03:01
ip addr add 10.3.0.1/24 brd + dev r3-eth0
ip addr add 10.0.4.2/24 brd + dev r3-eth1


echo 1 > /proc/sys/net/ipv4/ip_forward

# adding routes
ip route add 10.0.2.0/24 via 10.0.4.1 dev r3-eth1
ip route add 10.0.1.0/24 via 10.0.4.1 dev r3-eth1
ip route add 10.2.0.0/24 via 10.0.4.1 dev r3-eth1
ip route add 10.4.0.0/24 via 10.0.5.2 dev r3-eth3

