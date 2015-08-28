#!/usr/bin/env python

#liste des sockets dans /etc/services
# The Well Known Ports are those from 0 through 1023.
# The Registered Ports are those from 1024 through 49151
# The Dynamic and/or Private Ports are those from 49152 through 65535
#               5000        Unassigned
#               14415-14935 Unassigned

# sim_vehicle.sh (simulation SITL) :
# MAVPROXY TCP : 5760              5770
# MAVPROXY UDP : 14550             14560
# SITL         : 5501 5002 5003    5511 5512 5513
# skywritting  : 14548 14549

# Pour verifier les ports ouverts 
# lsof -i UDP     -> list opened udp ports
# Network Utility -> scan port

import socket

def Main():
#    host = 'localhost'
    host = '127.0.0.1'
    port = 14549

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print "Server Started."
    data, addr = s.recvfrom(1024)
    print "From: " + str(addr) + " DATA: " + str(data)
    while True:
       data, addr = s.recvfrom(1024)
#      print "From: " + str(addr) + " DATA: " + str(data)

#        data = str(data).upper()
#        print "sending: " + str(data)
#        s.sendto(data, addr)
    s.close()

if __name__ == '__main__':
    Main()
