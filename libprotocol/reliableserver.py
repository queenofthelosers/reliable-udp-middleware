import json
import base64
import socket

bufferSize  = 1024

class ReliableServer:
    def est_connection(self,sockfd):
        bytesAddressPair = sockfd.recvfrom(bufferSize)
        msg_from_client = json.loads(base64.b64decode(bytesAddressPair[0]))
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(msg_from_client)
        print(clientMsg)
        conn_state = 0
        if(msg_from_client["SYN"]==1):
            #print("reached")
            response = {"SYN":1,"ACK":1}
            response = json.dumps(response)
            response = response.encode("utf-8")
            #print("obj:",response)
            response = base64.b64encode(response)
            sockfd.sendto(response, address)
            bytesAddressPair = sockfd.recvfrom(bufferSize)
            msg_from_client = json.loads(base64.b64decode(bytesAddressPair[0]))
            print("message from client:",msg_from_client)
            conn_state = 1
        if(msg_from_client["ACK"]==1 and conn_state==1):
            print("Connection Established with Client")
