from rudp_protocol import RUDP
import pickle
r = RUDP("127.0.0.1",9002,True)
r.connect_sock("127.0.0.1",9001)
while True:
    data, address = r.sock.recvfrom(1024)
    data = pickle.loads(data)
    print(data)




