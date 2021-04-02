from libprotocol.reliableserver import ReliableServer
from libprotocol.reliablesocket import ReliableSocket
import socket
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
serverAddressPort   = ("127.0.0.1", 20001)

# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.bind((localIP, localPort))

serverSocket = ReliableSocket(ip=localIP,port=localPort)
print("UDP server up and listening")
rs = ReliableServer()



while(True):
    rs.est_connection(serverSocket)

