#!/bin/bash

echo "Setting up Router"

ifconfig r4-eth0 0
ifconfig r4-eth1 0

ifconfig r4-eth0 hw ether 00:00:00:00:04:01
ifconfig r4-eth1 hw ether 00:00:00:00:04:02

ip addr add 10.4.0.1/24 brd + dev r4-eth0
ip addr add 10.0.5.2/24 brd + dev r4-eth1

echo 1 > /proc/sys/net/ipv4/ip_forward