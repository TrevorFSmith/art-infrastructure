from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import thread
import time
import datetime

host = '127.0.0.1'
port = 4352
buff = 512
addr = (host, port)

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(addr)
serversocket.listen(10)

clients = [serversocket]

def handler(clientsocket, clientaddr):

    print "Accepted connection from: ", clientaddr

    while True:
        data = clientsocket.recv(buff)

        if not data:
            break
        else:
            print("%s" % data)

        if "%1AVMT ?" == data:
            clientsocket.send("%1AVMT 11\\r\n")
        elif "%1POWR ?" == data:
            clientsocket.send("%1POWR 0\\r\n")
        elif "%1POWR 0" == data:
            clientsocket.send("%1POWR 0\\r\n")
        elif "%1POWR 1" == data:
            clientsocket.send("%1POWR 1\\r\n")
        elif "%1NAME ?" == data:
            clientsocket.send("%1NAME ERR3\\r\n")
        elif "%1INF1 ?" == data:
            clientsocket.send("%1INF1 ERR3\\r\n")
        elif "%1INF2 ?" == data:
            clientsocket.send("%1INF2 ERR3\\r\n")
        elif "%1INFO ?" == data:
            clientsocket.send("%1INFO ERR3\\r\n")
        elif "%1LAMP ?" == data:
            clientsocket.send("%1LAMP 500\\r\n")


    clients.remove(clientsocket)
    clientsocket.close()


def push():
    while True:
        for i in clients:
            if i is not serversocket:
                i.send("%1LAMP 500\\r\n")
        time.sleep(10)


thread.start_new_thread(push, ())


while True:
    try:
        print "Server is listening for connections\n"
        clientsocket, clientaddr = serversocket.accept()
        clients.append(clientsocket)
        thread.start_new_thread(handler, (clientsocket, clientaddr))
    except KeyboardInterrupt:
        print "Closing server socket..."
        serversocket.close()
