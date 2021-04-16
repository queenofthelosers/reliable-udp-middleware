import sys
import os
sys.path.append("../")
from protocol_files.rudp_copy_protocol import RUDP


r = RUDP("127.0.0.1", 9001, False)
r.connect_sock("127.0.0.1", 9002)
r.listen()


