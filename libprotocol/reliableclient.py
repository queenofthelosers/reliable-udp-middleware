import pickle
import base64
import socket
import time

serverAddressPort   = ("127.0.0.1", 20001)
bufferSize  = 1024
localIP     = "127.0.0.1"
localPort   = 20002

class ReliableClient:
    def est_connection(self,payload,sockfd):
        open = True
        while True:
            try:
                client_bytes = pickle.dumps(payload)
                if open==True:
                    time.sleep(10)
                    open=False
                sockfd.sock.sendto(client_bytes,serverAddressPort)
                msgFromServer = sockfd.sock.recvfrom(bufferSize)
                msgFromServer = pickle.loads(msgFromServer[0])
                print(msgFromServer)
                if(msgFromServer["SYN"]==1 and msgFromServer["ACK"]==1):
                    payload = {"ACK":1}
                    payload_bytes = pickle.dumps(payload)
                    sockfd.sock.sendto(payload_bytes,serverAddressPort)
                    print("Connection Established")
                    sockfd.sock.settimeout(None)
                    break
                    #sockfd.sock.close()
                
            except Exception as e:
                print(" Client error in connection,",e)
                continue
            # finally:
            #     self.est_connection(payload,sockfd)
            
            

    