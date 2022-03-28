#!/bin/bash

echo "Setting up Router"
ifconfig r1-eth0 0
ifconfig r1-eth1 0
ifconfig r1-eth2 0
ifconfig r1-eth0 hw ether 00:00:00:00:01:01
ifconfig r1-eth1 hw ether 00:00:00:00:01:02
ifconfig r1-eth2 hw ether 00:00:00:00:01:03
ip addr add 10.0.1.1/24 brd + dev r1-eth0
ip addr add 10.0.2.1/24 brd + dev r1-eth1
ip addr add 10.0.6.1/24 brd + dev r1-eth2
echo 1 > /proc/sys/net/ipv4/ip_forward

# adding route's with other hosts destination
ip route add 10.2.0.0/24 via 10.0.6.2 dev r1-eth2
ip route add 10.3.0.0/24 via 10.0.6.2 dev r1-eth2
ip route add 10.4.0.0/24 via 10.0.6.2 dev r1-eth2


