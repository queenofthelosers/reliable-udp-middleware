import sys
import os
sys.path.append("../")
from protocol_files.rudp_copy_protocol import RUDP
import time

def chunks(lst, n):
    "Yield successive n-sized chunks from lst"
    list = []
    for i in range(0, len(lst), n):
        end = min(i + n, len(lst))
        list.append(lst[i:end])
    return list

print("im in client")
filename = sys.argv[1]
filesize = os.path.getsize(filename)
data = (filename, filesize)

r = RUDP("127.0.0.1", 9001, False)
r.connect_sock("127.0.0.1", 9002)
r.listen()
while(r.is_conn_est == False):
    pass
r.send(data)
with open(filename, "rb") as f:
    contents = f.read()
    # print(contents)
    list1 = chunks(contents, 2048)
    for chunk in list1:
        # print("chunk from client :", chunk)
        r.send(chunk)
r.disconnect()