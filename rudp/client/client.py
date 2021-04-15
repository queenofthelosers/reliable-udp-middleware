import sys
import os
sys.path.append('../')
from protocol_files.rudp_copy_protocol import RUDP



def chunks(lst, n):
    "Yield successive n-sized chunks from lst"
    list = []
    for i in range(0, len(lst), n):
        end = min(i+n, len(lst))
        list.append(lst[i:end])
    return list


filename = input("Enter Filename: ")
filesize = os.path.getsize(filename)
data = (filename, filesize)

r = RUDP("127.0.0.1", 9001, False)
r.connect_sock("127.0.0.1", 9002)
r.listen()

r.send(data)
with open(filename, "rb") as f:
    contents = f.read()
    print(contents)
    list1 = chunks(contents, 2048)
    for chunk in list1:
        print("chunk from client :", chunk)
        r.send(chunk)

