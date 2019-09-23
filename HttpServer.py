#!/usr/bin/python3
import socket
import sys
import os.path
from urllib.parse import urlparse
import re


TCP_IP = 'localhost'
TCP_PORT = 2500
BUFFER_SIZE = 1024

HTTP_Version = "HTTP/1.1"

def reqLineParser(req):
    requestLine = re.match("^(...) (/.*) (........)\s", req.decode())
    print(requestLine[0])
    method = requestLine[1]
    reqPath = requestLine[2]
    httpV = requestLine[3]
    return method, reqPath, httpV


def getResponse(reqPath, root):
    fobj = open(root + reqPath, "r")


    response = HTTP_Version + " 200 OK\r\n\r\n"
    response += fobj.read()
    return response





def listenerLoop(sock, root):

    while True:
        clientsock, clientaddr = sock.accept()
        print('Eingehende Verbindung von ', clientaddr)

        req = clientsock.recv(BUFFER_SIZE)
        if not req:
            break
        print(req.decode())
        method, reqPath, httpV = reqLineParser(req)
        if method == "GET":
            response = getResponse(reqPath, root)
        else:
            a=1
        print(response.encode('utf-8'))
        clientsock.send(response.encode())
        clientsock.close()

        return req



try:
    if len(sys.argv) != 2:
        print(sys.argv)
        raise ValueError("Invalid number of Arguments")
    print(sys.argv[1]+"/responses/404.html")
    if not os.path.exists(sys.argv[1]+"/responses/404.html"):
        raise ValueError("Path deoes not exist!")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))#
    print("Listening to Port: ", TCP_PORT)
    sock.listen()
    listenerLoop(sock, sys.argv[1])
    sock.close()

except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback
    traceback.print_exc()











