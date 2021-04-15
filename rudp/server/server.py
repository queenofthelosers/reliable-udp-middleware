import sys
sys.path.append('../')
from protocol_files.rudp_copy_protocol import RUDP
import pickle
r = RUDP("127.0.0.1",9002,True)
r.connect_sock("127.0.0.1",9001)
with open("acopy.txt","w") as f:
    while True:
        # data = pickle.loads(data)
        #print("Printing from server program :",data)
        r.listen()
        data = r.recv()
        f.write(data["data"])    