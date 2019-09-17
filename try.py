#!/usr/bin/python3


# Um Sockets verwenden zu kÃ¶nnen, mÃ¼ssen wir das socket Modul importieren
import socket
import sys
from urllib.parse import urlparse
import re




try:
    if  len(sys.argv) != 3 :
        raise Exception("Invalid number of Arguments")

    urlElements = urlparse(sys.argv[1])

    print('urlElements', urlElements)



    # Wir erzeugen einen Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wir verbinden uns mit dem Server (Host: google.at, Port: 80)
    sock.connect((urlElements[1], 80))

    # Wir senden eine Anfrage an den Server
    # Python3 verwendet intern Unicode-Strings, Ã¼ber das Netzwerk kÃ¶nnen wir nur Byte-Strings schicken
    # daher mÃ¼ssen wir Python-String mit encode('<codec>') in einen Byte-String umwandeln

    requestString = 'GET / HTTP/1.0\r\nhost: ' + urlElements[1] + '\r\n\r\n'
    print('requeststring ', requestString.encode("utf-8"))
    sock.send(requestString.encode("utf-8"))
    # sock.send('GET / HTTP/1.1\r\nhost: www.google.at\r\n\r\n'.encode("utf-8"))

    # Wir empfangen die Antwort vom Server
    # Als BuffergrÃ¶ÃŸe verwenden wir 2048, wenn die Nachricht grÃ¶ÃŸer ist, mÃ¼ssen wir recv() mehrmals aufrufen
    response = sock.recv(4048)

    # Wir geben die Antwort aus
    # Um einen Byte-String in einen Unicode-String umzuwandeln, mÃ¼ssen wir decode() aufrufen
    # print(response.decode())
    requestStatus = re.match(response, "HTTP/\d\.\d (\d+)")
    print(requestStatus)

    # print(re.match(response, "HTTP/(\d\.\d) (\d+) (\w+)\\r\\n.*Cache-Control:"))

    # Nicht vergessen alle Ressourcen wieder zu schlieÃŸen
    sock.close()

except:
    print("Ein Fehler ist aufgetreten")
    # Gebe die Exception und einen Stacktrace fÃ¼r die Fehlersuche aus
    import traceback
    traceback.print_exc()