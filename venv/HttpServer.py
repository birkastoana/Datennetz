#!/usr/bin/python3
import socket
import sys
from urllib.parse import urlparse
import re


TCP_IP = 'localhost'
TCP_PORT = 2500
BUFFER_SIZE = 1024

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen()

    clientsock, clientaddr = sock.accept()
    print('Eingehende Verbindung von ', clientaddr)

    sock.close()


except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback
    traceback.print_exc()