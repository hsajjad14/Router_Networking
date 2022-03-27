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

