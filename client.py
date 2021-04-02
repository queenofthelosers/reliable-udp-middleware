from libprotocol.reliableclient import ReliableClient
import socket
import time
from itertools import count
from multiprocessing import Process

localIP     = "127.0.0.1"
localPort   = 20002
bufferSize  = 1024
serverAddressPort   = ("127.0.0.1", 20001)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind((localIP, localPort))
connection_payload = {"SYN":1}
rc = ReliableClient()
rc.est_connection(connection_payload,UDPClientSocket)
