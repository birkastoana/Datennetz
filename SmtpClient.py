#!/usr/bin/python3
import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 25
BUFFER_SIZE = 1024
MESSAGE_TERMINATOR = b"\r\n.\r\n"
# This function will avoid escaping of dots in the msg body for smtp protocol
def stringPreparer(bodyString):
    try:
        prepareString = bodyString.split(b'\n.')
        n = 0
        for i in prepareString:
            if n != 0:
                prepareString[n] = b'\n..' + i
            n += 1
        return prepareString
    except:
        return None
# Takes a file path relativ to the script location
def fileHandler(filePath):
    try:
        fobj = open(filePath, "r")
        return stringPreparer(fobj.read().encode())
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

    sock.send(b"EHLO christian\r\n")
    response = sock.recv(BUFFER_SIZE)
    if response[:3] != b'250': raise Exception("Error try to connect mailserver")


    sock.send(b"MAIL FROM: " + mailFrom + b"\r\n")
    response = sock.recv(BUFFER_SIZE)
    if response[:3] != b'250': raise Exception("Error: invalid sender adress: " + mailFrom.decode())

    sock.send(b"RCPT TO: " + rcptTo +  b"\r\n")
    response = sock.recv(BUFFER_SIZE)
    if response[:3] != b'250': raise Exception("Error: invalid receiver adress: " + rcptTo.decode())

    sock.send(b"DATA\r\n")
    response = sock.recv(BUFFER_SIZE)

    sock.send(b"Subject: " + subjectString + b"\r\n")
    for item in msgBody:
        sock.send(item)
    sock.send(MESSAGE_TERMINATOR)

    response = sock.recv(BUFFER_SIZE)
    sock.send(b"QUIT")
except:
    print("Ein Fehler ist aufgetreten")
    import traceback
    traceback.print_exc()

finally:
    if sock is not None: sock.close()