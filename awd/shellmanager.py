#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import time
import random

HOST = '0.0.0.0'
PORT = 23333
BUFSIZE = 1024 * 8

VER = sys.version_info.major

if VER == 3:
    raw_input = input


class Reader(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.stop = False

    def run(self):
        while not self.stop:
            data = self.client.recv(BUFSIZE)
            if data:
                print(data)
            time.sleep(1)
            continue

    def cmd(self, cmd):
        self.client.sendall(cmd)

    def stop(self):
        self.stop = True

x = {
    "127.0.0.1": {
        "port": "c"
    }
}


class Listener(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.clients = {}
        self.stop = False
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, port))
        self.sock.listen(1)

    def run(self):
        print("listener started %s\n" % self.port)
        while not self.stop:
            client, cltadd = self.sock.accept()
            t = Reader(client)
            c_host = str(client.getpeername()[0])
            c_port = client.getpeername()[1]
            if c_host not in self.clients:
                self.clients.update({c_host: {c_port: t}})
            else:
                self.clients[c_host].update({c_port: t})
            t.start()

    def stop(self):
        for i in self.clients:
            self.clients[i][1].stop()
        self.stop = True


def cmd(lst):
    cmd = raw_input("cmd > ")
    while True:
        try:
            if cmd == 'ls':
                for k_host in lst.clients:
                    print(">>  %s\n" % (k_host))
                    for k_port in lst.clients[k_host]:
                        print(">>>>  %s -> %s\n" %
                              (k_port, lst.clients[k_host][k_port]))
            elif cmd[:4] == 'fuck':
                cc = cmd[5:].strip()
                cc = cc.split(":")
                host = cc[0]
                port = cc[1]
                if host and lst.clients[host]:
                    client = lst.clients[host][port]
                    pt = "client %s:%d >>" % (host, port)
                    ccmd = raw_input(pt)
                    while ccmd:
                        if ccmd == "vquit" or ccmd == "vq":
                            break
                        client.sendall(ccmd + "\n")
                        ccmd = ""
                        ccmd = raw_input(pt)
            elif cmd == 'exit':
                lst.stop()
                break
            elif cmd[:4] == 'eval':
                eval(cmd[4:])
            else:
                print("cmd :\n\tls\n\tfuck [n]\n\texit")
            # TODO test-live
            cmd = raw_input("cmd > ")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    lst = Listener(PORT)
    lst.daemon = True
    lst.start()
    cmd(lst)
