#!/usr/bin/python3


# Um Sockets verwenden zu kÃ¶nnen, mÃ¼ssen wir das socket Modul importieren
import socket
import sys
from urllib.parse import urlparse
import re




try:
    if  len(sys.argv) != 3 :
        print(sys.argv)
        raise Exception("Invalid number of Arguments")

    urlElements = urlparse(sys.argv[1])
    print ("urlelements: " ,  urlElements)

    # verwende die variablen, weil die urlElements spaeter ggf ueberschrieben werden!
    path = urlElements[2]
    params = urlElements[3]
    query = urlElements[4]

    loopFlag = 1
    while loopFlag:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((urlElements[1], 80))
        print("++++++++++++++++++++++")
        print(urlElements[1])
        print("++++++++++++++++++++++")

        requestString = 'GET '  + path
        if len(query) != 0: requestString = requestString + '?' + query
        requestString = requestString + " HTTP/1.1\r\nHost: " + urlElements[1] +"\r\n\r\n"

        print("~~~~~~~~~~~~~~~")
        print('requeststring ', requestString.encode("utf-8"))

        print("~~~~~~~~~~~~~~~")
        sock.send(requestString.encode("utf-8"))
        response = sock.recv(4048)

        response = response.split(b"\r\n\r\n")
        head = response[0]
        body = response[1]
        print(head)

        requestStatus = re.match(b"HTTP/\d*\.\d* (\d+)", head)
        statusCode = requestStatus[1].decode()

        if statusCode == "200":
            print("********** entered status 200 ***********")
            loopFlag = 0
        elif statusCode[0] == "3":
            print(statusCode[0])
            print("********** entered status 3xx ***********")
            newAdress = re.match(".*\sLocation: (.*)\s.*", head.decode())
            urlElements = urlparse(newAdress[1])
        elif statusCode[0] == "4" or statusCode[0] == "5":
            print("********** entered error  ***********")
            error = re.match("HTTP/\d.\d (.*)\s.*", head.decode())
            print(error[1])
            raise Exception(error[1] + requestString)





        sock.close()



except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback
    traceback.print_exc()