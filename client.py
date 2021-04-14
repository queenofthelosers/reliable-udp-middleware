from libprotocol.reliableclient import ReliableClient
import socket
from libprotocol.reliablesocket import ReliableSocket

localIP = "127.0.0.1"
localPort = 20002
bufferSize = 1024
serverAddressPort = ("127.0.0.1", 20001)

# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket = ReliableSocket(ip=localIP, port=localPort)

connection_payload = {"SYN": 1}
rc = ReliableClient()
rc.est_connection(connection_payload, clientSocket)
clientSocket.sock.close()
# clientSocket.sock.shutdown(socket.SHUT_WR)
# clientSocket.sock.shutdown()
