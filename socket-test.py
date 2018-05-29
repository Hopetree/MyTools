# -*- coding: utf-8 -*-
import socket
import threading
import queue

def ConnectFunc(host):
    while not q.empty():
        port  = q.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            print('[+] {} open'.format(port))
            s.close()
        except Exception as e:
            pass

if __name__ == '__main__':
    q = queue.Queue()
    for i in [22,80,]:
        q.put(i)
    ths = []
    host = '119.23.106.34'
    for p in range(20):
        t = threading.Thread(target=ConnectFunc, args=(host,))
        t.start()
        ths.append(t)
    for t in ths:
        t.join()
    print('over !')
