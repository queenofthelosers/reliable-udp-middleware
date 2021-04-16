import sys
import time
sys.path.append("../")
from protocol_files.rudp_copy_protocol import RUDP
import pickle
import csv

tic=time.time()
r = RUDP("127.0.0.1", 9002, True)
r.connect_sock("127.0.0.1", 9001)
r.listen()
r.establish_conn()
# data = r.recv()
# filename, filesize = data["data"]
# print("Receiving ", filename, filesize)
# recv_size = 0
# with open(filename, "wb") as f:
#     while True:
#         data = r.recv()
#         recv_size += len(data["data"])
#         f.write(data["data"])
#         if recv_size >= filesize:
#             toc=time.time()
#             elapsed_time=toc-tic
#             throughput=filesize/elapsed_time
#             print("Throughput in bytes/sec ",throughput)

#             with open(sys.argv[1]+'.csv', 'a') as file:
#                 csvwriter = csv.writer(file)
#                 csvwriter.writerow([sys.argv[2],throughput]) 
#             r.disconnect()
#             break
