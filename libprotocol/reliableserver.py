import pickle
import base64
import socket
import time
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
    
class ReliableServer:
    def est_connection(self,sockfd):
        #sockfd.settimeout(5)
        try:
            bytesAddressPair = sockfd.sock.recvfrom(bufferSize)
            msg_from_client = pickle.loads((bytesAddressPair[0]))
            address = bytesAddressPair[1]
            clientMsg = "Message from Client:{}".format(msg_from_client)
            #time.sleep(10)
            print(clientMsg)
            conn_state = 0
            if(msg_from_client["SYN"]==1):
                #print("reached")
                response = {"SYN":1,"ACK":1}
                response = pickle.dumps(response)
                sockfd.sock.sendto(response, address)
                bytesAddressPair = sockfd.sock.recvfrom(bufferSize)
                msg_from_client = pickle.loads((bytesAddressPair[0]))
                print("message from client:",msg_from_client)
                conn_state = 1
            if(msg_from_client["ACK"]==1 and conn_state==1):
                print("Connection Established with Client")
        except:
            print("Error in connection")

            
