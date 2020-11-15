#!/bin/bash
# Connect to the internet, run as sudo and required on restart
sudo /sbin/route add default gw 192.168.7.1
echo 'echo "nameserver 8.8.8.8" >> /etc/resolv.conf' | sudo -s

