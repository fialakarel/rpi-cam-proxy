#!/usr/bin/python3

# author:   Karel Fiala
# email:    fiala.karel@gmail.com

from socket import *   
from threading import Thread
import sys

BUFSIZE = 4096 # buffer size for data

def newclient():
    global serv2
    global clients
    global dx

    try:
        while True:
            conn, addr = serv2.accept() #accept the connection
            clients.append(conn)
            if dx != "":
                conn.send(dx)   # HACK -- for faster detection
    except KeyboardInterrupt:
        sys.exit(0)


if len(sys.argv) != 3:
    print("ERR: <script> <port-for-cam> <port-for-clients>")
    sys.exit(1)

serv = socket( AF_INET,SOCK_STREAM)
serv.bind(('0.0.0.0', int(sys.argv[1])))
serv.listen(1)

serv2 = socket( AF_INET,SOCK_STREAM)
serv2.bind(('0.0.0.0', int(sys.argv[2])))
serv2.listen(10)

clients = list()

Thread(target=newclient).start()

#socket.setblocking(0)

try:
    while True:
        first=1
        dx=""
        serv.settimeout(None)
        conn, addr = serv.accept() #accept the connection
        serv.settimeout(1.0)

        while True:
            if first:
                data = conn.recv(32)
                dx = data
                first=0
            else:
                data = conn.recv(BUFSIZE)

            if not data:
                break

            for x in clients:
                try:
                    x.send(data)
                except:
                    clients.remove(x)
except KeyboardInterrupt:
    sys.exit(0)


