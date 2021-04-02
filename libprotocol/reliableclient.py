import json
import base64
import socket


serverAddressPort   = ("127.0.0.1", 20001)
bufferSize  = 1024

class ReliableClient:
    def est_connection(self,payload,sockfd):
        client_msg = json.dumps(payload)
        client_bytes = client_msg.encode("utf-8")
        client_bytes = base64.b64encode(client_bytes)
        
        sockfd.sendto(client_bytes,serverAddressPort)
        msgFromServer = sockfd.recvfrom(bufferSize)
        msgFromServer = base64.b64decode(msgFromServer[0])
    
        msgFromServer = json.loads(msgFromServer)
        print(msgFromServer)
        if(msgFromServer["SYN"]==1 and msgFromServer["ACK"]==1):
            payload = {"ACK":1}
            payload = json.dumps(payload)
            payload_bytes = payload.encode("utf-8")
            payload_bytes = base64.b64encode(payload_bytes)
            sockfd.sendto(payload_bytes,serverAddressPort)
            print("Connection Established")
            

    