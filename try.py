#!/usr/bin/python3
import socket
import sys
from urllib.parse import urlparse
import re
try:
    if len(sys.argv) != 3:
        print(sys.argv)
        raise Exception("Invalid number of Arguments")
    urlElements = urlparse(sys.argv[1])
    path = urlElements[2]
    params = urlElements[3]
    query = urlElements[4]
    loopFlag = 1
    while loopFlag:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((urlElements[1], 80))
        requestString = 'GET ' + urlElements[2]
        if len(urlElements[2]) == 0: requestString = requestString + "/"
        if len(urlElements[4]) != 0: requestString = requestString + '?' + query
        requestString = requestString + " HTTP/1.1\r\nHost: " + urlElements[1] + "\r\n\r\n"
        sock.send(requestString.encode("utf-8"))
        response = sock.recv(4048)
        response = response.split(b"\r\n\r\n")
        head = response[0]
        body = response[1]
        body = body.split(b'\r\n')
        bodySize = body[0]
        body = body[len(body)-1]
        requestStatus = re.match(b"HTTP/\d*\.\d* (\d+)", head)
        statusCode = requestStatus[1].decode()
        if statusCode == "200":
            print("request successfull! Save body to ", sys.argv[2])
            n = 0
            fobj = open(sys.argv[2], 'w+b')
            while body != b'':
                fobj.write(body)
                n += 1
                body = sock.recv(4048)
            fobj.close()
            loopFlag = 0
        elif statusCode[0] == "3":
            newAdress = re.search(b".*Location: (.*)\r", head)
            urlElements = urlparse(newAdress[1].decode())
        elif statusCode[0] == "4" or statusCode[0] == "5":
            error = re.match("HTTP/\d.\d (.*)\s.*", head.decode())
            print(error[1])
            raise Exception(error[1] + requestString)
        sock.close()

except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback
    traceback.print_exc()