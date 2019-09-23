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
    if reqPath == "/":
        reqPath = "/index.html"
    print(method)
    print(reqPath)
    print(httpV)
    return method, reqPath, httpV


def getResponse(reqPath, root, status):
    try:
        print("try to open", root + reqPath)
        fobj = open(root + reqPath, "r")
    except:
        fobj = open(root + "/404.html", "r")
        status = "404 Not Found"
    finally:
        response = HTTP_Version + " " + status + "\r\n\r\n"
        response += fobj.read()
        return response


def listenerLoop(sock, root):
    while True:
        status = "200 OK"
        try:
            clientsock, clientaddr = sock.accept()
            print('Eingehende Verbindung von ', clientaddr)

            req = clientsock.recv(BUFFER_SIZE)
            if not req:
                break
            print(req.decode())
            method, reqPath, httpV = reqLineParser(req)
            if method == "GET":
                print("************************")
                print(reqPath)
                print(root)
                print(status)

                response = getResponse(reqPath, root, status)
            else:
                a = 1
            print(response.encode('utf-8'))

        except:
            response = getResponse("/500.html", root, "500 Internal Server Error")
        finally:
            clientsock.send(response.encode())
            clientsock.close()



try:
    if len(sys.argv) != 2:
        print(sys.argv)
        raise Exception("Invalid number of Arguments")
    root = sys.argv[1] + "/responses"
    if not os.path.exists(root + "/404.html"):
        raise Exception("Path deoes not exist!")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))  #
    print("Listening to Port: ", TCP_PORT)
    sock.listen()
    listenerLoop(sock, root)
    sock.close()

except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback

    traceback.print_exc()
