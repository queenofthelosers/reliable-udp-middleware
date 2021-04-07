import socket
import pickle
import time
import random
import builtins
import hashlib
from copy import deepcopy
from collections.abc import Hashable
from threading import Thread, Lock
from rudp_packet import Packet
'''
PACKET STRUCTURE
  pkt = {
      "SYN": 1,
      "ACK" : 1,
      "FIN" : 1,
      "KAL" : 1,
      "CHK" : 1,
      "seq" : 25,
      "data" :  "asodfoaisdf",
      "acknum" : ,
      "chksum" :    
 }
'''

class RUDP:
    def __init__(self, hostname, port, isServer):
        self.hostname = hostname
        self.port = port
        self.sock = self.initialize_socket(hostname,port,isServer)
        self.recv_window = []
        self.send_window = []
        self.curr_seq = 0
        self.expiry_timestamp = 0
        self.is_connected = False
        self.recv_map = {}
        self.BUFFSZ = 1050
        self.PKTSZ = 1024
        self.WINDOWSZ = 1024
        self.TIMEOUT = 3
        self.KAL_TIMEOUT = 30
        self.transmit_lock = Lock()
        self.socket_lock = Lock()
        self.seq_num_lock = Lock()
        self.BLOCKING_TIME = 0.00005

    def initialize_socket(self, hostname, port , isServer = True):
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockfd.bind((hostname, port))
        return sockfd

    def retransmit(self):
        while True:
            time.sleep(self.TIMEOUT)

            if self.is_connected == True:
                self.transmit_lock.acquire()
                try:
                    print("Starting Retransmission...")
                    for send_window_item in self.send_window:
                        elapsed_time = time.time() - send_window_item["time"]

                        if elapsed_time >= self.TIMEOUT:
                            print("Retransmitting: ", send_window_item["packet"].seqNum)
                            self.write_to_sock(send_window_item["packet"], is_retransmit=True)
                finally:
                    self.transmit_lock.release()

    def keep_alive(self):
        
        while True:
            time.sleep(self.TIMEOUT)
            tic = time.time() - self.send_window[-1]["time"] 
            if(tic > self.KAL_TIMEOUT):
                self.disconnect()
            
            
    def connect_sock(self, hostname, port):
        self.sock.connect((hostname,port))
        print("Connected")
        
    def get_next_seq(self):
        self.seq_num_lock.acquire()
        try:
            self.curr_seq = self.curr_seq+1
        finally:
            self.seq_num_lock.release()
        return self.curr_seq

    def disconnect(self):
        pass

    def update_seq(self):
        pass

    def listen(self):
        pass

    def listen_helper(self):
        pass

    def read_from_sock(self):
        pass
    def write_to_sock(self, packet,is_retransmit=False):
        
        send_window_item = {
            "packet" : packet,
            "time" : time.time(),
        }

        if not is_retransmit:
            self.transmit_lock.acquire()
            try:
                self.send_window.append(packet)
            finally:
                self.transmit_lock.release()
            
        serialized_packet = packet.serialize_packet()
        self.socket_lock.acquire()
        try:
            self.sock.sendall(serialized_packet)
        finally:
            self.socket_lock.release()

    # def recv(self, blocking=True):
    #     if blocking == True:
    #         while True:
    #             data = self.__read_socket()
    #             if data != None:
    #                 data = deepcopy(data)
    #                 return data
    #             time.sleep(FSSP.BLOCKING_SLEEP)
    #     else:
    #         data = self.__read_socket()
    #         data = deepcopy(data)
    #         return data

    def send(self, data, control_bits ={"SYN":0, "ACK":0, "ACKNUM":0,"FIN":0,"CHK":0,"KAL":1}):
        while True :
            if (len(self.send_window) < self.WINDOWSZ):
                break
            else :
                print("Receive window is full")
                time.sleep(self.BLOCKING_TIME)

        seq = self.get_next_seq()
        data_copy = deepcopy(data)    # if user modify the object, the shouldn't be changed
        packet = Packet(data = data_copy,control_bits = control_bits, seqNum = seq)
        self.write_to_sock(packet)
        return True