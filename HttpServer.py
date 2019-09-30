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

# reqLineParser will take the request string and give back method, path to resource and httpVersion
# if the path is root, this function will return the path to index.html
# if there is no explicit file requested, the function will resolute the path to a .html file
def reqLineParser(req):
    requestLine = re.match("^(...) (/.*) (........)\s", req.decode())
    method = requestLine[1]
    reqPath = requestLine[2]
    httpV = requestLine[3]
    if reqPath == "/":
        reqPath = "/index.html"
    elif reqPath.find(".html") < 1:
        if reqPath[len(reqPath)-1] == '/':
            reqPath = reqPath[:len(reqPath)-1]
        reqPath = reqPath + ".html"

    return method, reqPath, httpV

# this function will try to open the source and return a string containing the
# whole response header + body
def getResponse(reqPath, root, status):
    try:
        if reqPath == "/shutdown.html":
            return -1
        fobj = open(root + reqPath, "r")
    except:
        fobj = open(root + "/404.html", "r")
        status = "404 Not Found"
    finally:
        if reqPath == "/shutdown.html":
            return -1
        response = HTTP_Version + " " + status + "\r\n\r\n"
        response += fobj.read()
        return response

# listenerLoop listens to the port and waits for a client request
# if the response is sent, the loop begins to wait for the next request
def listenerLoop(sock, root):
    runningFlag = True
    while runningFlag:
        status = "200 OK"
        try:
            clientsock, clientaddr = sock.accept()
            print('Eingehende Verbindung von ', clientaddr)

            req = clientsock.recv(BUFFER_SIZE)

            if not req:
                continue
            method, reqPath, httpV = reqLineParser(req)
            if method == "GET":
                response = getResponse(reqPath, root, status)
            else:
                raise Exception

        except:
            response = getResponse("/500.html", root, "500 Internal Server Error")
        finally:
            if response == -1:
                return
            clientsock.send(response.encode())
            clientsock.close()




try:
    if len(sys.argv) != 2:
        raise Exception("Invalid number of Arguments")
    root = sys.argv[1] + "/responses"
    if os.path.exists(root + "/404.html") < 0:
        raise Exception("Path deoes not exist!", root)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))  #
    print("Listening to Port: ", TCP_PORT)
    print("For shutdown call <host>/shutdown")
    sock.listen()
    listenerLoop(sock, root)
    sock.close()

except:
    sock.close()
    print("Ein Fehler ist aufgetreten")
    import traceback
    traceback.print_exc()
