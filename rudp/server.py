from rudp_protocol import RUDP
import pickle
r = RUDP("127.0.0.1",9002,True)
r.connect_sock("127.0.0.1",9001)
r.listen()
while True:
    data = r.recv()
    # data = pickle.loads(data)
    print("Printing from server program :",data)




