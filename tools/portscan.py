#!/bin/env python
# -*- encoding: utf-8 -*-

from socket import *

__info__ = {
    "desc": "A script for scan port",
    "version": "1.0",
    "usage": "ip port[,more] [timeout]"
}

status = {
    0: "open",
    10049: "address not available",
    10061: "closed",
    10060: "timeout",
    10056: "already connected",
    10035: "filtered",
    11001: "IP not found",
    10013: "permission denied"
}

PORT_TABLE = {
    21: "FTP",
    22: "SSH",
    23: "Telent",
    80: "HTTP",
    443: "HTTPS",
    1521: "Oracle Server",
    3306: "MySQL Server",
    3389: "RDP"
}


def scan(ip, port, timeout):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))
    except:
        print "Cannot connect to IP"
        return
    s.close()
    if result in status.keys():
        return str(port) + " : " + PORT_TABLE[port] + " : " + status[result]
    else:
        return str(port) + " : " + PORT_TABLE[port] + " : " + str(result)


def run(arg):
    data = {
        "ip": "",
        "timeout": 5
    }
    if len(arg) < 2:
        return 'Error'
    data['ip'] = arg[0]
    ports = arg[1].split(",")
    if len(arg) > 3:
        data['timeout'] = int(arg[2])
    if len(ports) == 1:
        data['port'] = int(arg[1])
        return scan(**data)
    else:
        return [scan(port=int(i), **data) for i in ports]

if __name__ == '__main__':
    for i in range(256):
        print("192.168.5.%d" % i)
        print run(["192.168.5.%d" % i, "80"])
