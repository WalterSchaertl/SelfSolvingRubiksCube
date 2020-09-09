#!/bin/bash
# Connect to the internet, run as sudo and required on restart
sudo /sbin/route add default gw 192.168.7.1
echo 'echo "nameserver 8.8.8.8" >> /run/connman/resolv.conf' | sudo -s