#!/bin/bash

echo "Setting up Router"

ifconfig r3-eth0 0
ifconfig r3-eth1 0
ifconfig r3-eth2 0
ifconfig r3-eth3 0

ifconfig r3-eth0 hw ether 00:00:00:00:03:01
ifconfig r3-eth1 hw ether 00:00:00:00:03:02
ifconfig r3-eth2 hw ether 00:00:00:00:03:03
ifconfig r3-eth2 hw ether 00:00:00:00:03:04

ip addr add 10.3.0.1/24 brd + dev r3-eth0
ip addr add 10.0.4.2/24 brd + dev r3-eth1
ip addr add 10.0.3.2/24 brd + dev r3-eth2
ip addr add 10.0.5.1/24 brd + dev r3-eth3

echo 1 > /proc/sys/net/ipv4/ip_forward