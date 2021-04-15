import sys

sys.path.append("../")
from protocol_files.rudp_copy_protocol import RUDP
import pickle

r = RUDP("127.0.0.1", 9002, True)
r.connect_sock("127.0.0.1", 9001)
r.listen()
data = r.recv()
filename, filesize = data["data"]
print("Receiving ", filename, filesize)
recv_size = 0
with open(filename, "wb") as f:
    while True:
        data = r.recv()
        recv_size += len(data["data"])
        f.write(data["data"])
        if recv_size >= filesize:
            r.disconnect()
            break
