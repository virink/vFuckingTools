#!/user/bin python
# -*- coding:utf-8 -*-
# Author:Bing
# Contact:amazing_bing@outlook.com
# DateTime: 2017-01-17 19:06:06
# Description:  coding

import sys
sys.path.append("..")

import threading
import socket
import sys
import cmd
import os
import Queue
from core.settings import *

# 线程锁
lock = threading.Lock()

# 制作扫描端口队列


def GetQueue(host):
    PortQueue = Queue.Queue()
    for port in range(1, 65535):
        PortQueue.put((host, port))
    return PortQueue


class ScanThread(threading.Thread):

    def __init__(self, SingleQueue, outip):
        threading.Thread.__init__(self)
        self.setDaemon(True)  # 设置后台运行，让join结束
        self.SingleQueue = SingleQueue
        self.outip = outip

    def get_port_service(self, text):
        service_path = dict_script_path + "nmap-services.txt"
        port_server = str(text) + "/tcp"
        with open(service_path, "r") as server:
            for finger in server.readlines():
                port = finger.strip().split(";")[1]
                if port == port_server:
                    fingers = str(finger.strip().split(";")[0])
                    return (port_server, fingers)
            return (port_server, "unknown")

    def Ping(self, scanIP, Port):
        global OpenPort, lock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        address = (scanIP, Port)
        try:
            sock.connect(address)
        except:
            sock.close()
            return False
        sock.close()
        if lock.acquire():
            # print "IP:%s  Port:%d" % (scanIP, Port)
            self.outip.put(self.get_port_service(Port))
            lock.release()
        return True

    def run(self):
        while not self.SingleQueue.empty():
            # 获取扫描队列，并扫描
            host, port = self.SingleQueue.get()
            self.Ping(host, port)


class Work(object):

    def __init__(self, scan_id="", scan_target="", scan_type="", scan_args="", back_fn=None):
        self.scan_id = scan_id
        self.target = scan_target
        self.scan_type = scan_type
        self.args = scan_args
        self.back_fn = back_fn
        self.result = []

    def run(self):
        ThreadList = []
        # 扫描队列
        SingleQueue = GetQueue(self.target)
        # 存储结果队列
        resultQueue = Queue.Queue()
        # 启动200线程并发
        for i in range(0, 200):
            t = ScanThread(SingleQueue, resultQueue)
            ThreadList.append(t)
        for t in ThreadList:
            t.start()
        for t in ThreadList:
            # 需要设置线程为后台，然后没法结束；join等待结束后台线程
            t.join(0.1)

        data = []
        while not resultQueue.empty():
            line = resultQueue.get()
            data.append(
                {"bug_name": str(line[0]), "bug_summary": str(line[1])})
        result = {"status": 1, "data": data,
                  "scan_id": self.scan_id, "scan_type": "nmap"}
        self.back_fn(result)


def save(nmap_result):
    print nmap_result, "----------------"

if __name__ == '__main__':
    t = Work(scan_target="100tal.org", back_fn=save)
    t.run()
