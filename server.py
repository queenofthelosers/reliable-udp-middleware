from libprotocol.reliableserver import ReliableServer
import socket


localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
serverAddressPort   = ("127.0.0.1", 20001)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
rs = ReliableServer()
while(True):
    rs.est_connection(UDPServerSocket)
