#!/usr/bin/python3
import socket
import sys
import os.path
from urllib.parse import urlparse
import re


TCP_IP = '127.0.0.1'
TCP_PORT = 25
BUFFER_SIZE = 1024
MESSAGE_TERMINATOR = "\r\n.\r\n"

def pointfinder(bodyString):
    try:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(bodyString)
        abc = re.search(bodyString, '^(.*)\s(.*)')
        print(abc[1])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    except:
        import traceback
        traceback.print_exc()

def fileHandler(filePath):
    try:
        fobj = open(filePath, "r")
        pointfinder(fobj.read())
        return fobj.read()
    except:
        return None
    finally:
        fobj.close()



#  entry point:
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))

    # argument #1 sender andress
    # argument #2 receiver adress
    # argument #3 subject
    # argument #4 file path
    if len(sys.argv) != (1 + 4):
        raise Exception("Invalid number of Arguments")

    mailFrom = sys.argv[1].encode()
    rcptTo = sys.argv[2].encode()
    subjectString = sys.argv[3].encode()


    msgBody = fileHandler(sys.argv[4])
    if msgBody == None: raise NameError(sys.argv[4] + "\n ist ein ungültiger Dateipfad!")



    response = sock.recv(BUFFER_SIZE)
    if response[:3] != b'220': raise Exception("Error try to connect mailserver")
    print("1", response)

    sock.send(b"EHLO christian\r\n")
    response = sock.recv(BUFFER_SIZE)
    print(response)
    if response[:3] != b'250': raise Exception("Error try to connect mailserver")


    sock.send(b"MAIL FROM: " + mailFrom + b"\r\n")
    response = sock.recv(BUFFER_SIZE)
    if response[:3] != b'250': raise Exception("Error: invalid sender adress: " + mailFrom.decode())
    print(response)


    sock.send(b"RCPT TO: " + rcptTo +  b"\r\n")
    response = sock.recv(BUFFER_SIZE)
    print(response)
    if response[:3] != b'250': raise Exception("Error: invalid receiver adress: " + rcptTo.decode())

    sock.send(b"DATA\r\n")
    response = sock.recv(BUFFER_SIZE)
    print(response)

    sock.send(msgBody.encode())
    sock.send(MESSAGE_TERMINATOR.encode())
    response = sock.recv(BUFFER_SIZE)
    print(response)






except:

    print("Ein Fehler ist aufgetreten")
    import traceback
    traceback.print_exc()

finally:
    if sock is not None: sock.close()