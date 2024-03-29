#Team Members
#Shubh Deep 2018A7PS0162H
#Shivang Singh 2018A7PS0115H
#Nishit Chouhan 2018A7PS0446H
#Deepak George 2018A7PS0244H
import socket
import pickle
import time
import random
import builtins
import hashlib
from copy import deepcopy
from collections.abc import Hashable
from threading import Thread, Lock
from .rudp_packet import Packet
import sys

"""
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
"""


class RUDP:
    def __init__(self, hostname, port, isServer):
        self.hostname = hostname
        self.port = port
        self.sock = self.initialize_socket(hostname, port, isServer)
        self.recv_window = []
        self.send_window = []
        self.curr_seq = 0
        self.delivery_seq = self.curr_seq + 1
        self.expiry_timestamp = 0
        self.is_connected = False
        self.recv_map = {}
        self.BUFFSZ = 5000
        self.PKTSZ = 4096
        self.WINDOWSZ = 100000
        self.TIMEOUT = 5
        self.KAL_TIMEOUT = 20
        self.transmit_lock = Lock()
        self.send_lock = Lock()
        self.receive_lock = Lock()
        self.seq_num_lock = Lock()
        self.delivery_seq_lock = Lock()
        self.BLOCKING_TIME = 0.00005
        self.latest_packet_time = time.time()
        self.kal_count = 0
        self.kal_lock = Lock()
        self.listening_thread = 0
        self.kal_thread = 0
        self.retransmission_thread = 0
        self.is_conn_est = False

    def initialize_socket(self, hostname, port, isServer=True):
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockfd.bind((hostname, port))
        return sockfd

    def retransmit(self):
        while True:
            if self.is_connected == False:
                break
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
            if self.is_connected == False:
                break
            if time.time() - self.latest_packet_time >= self.KAL_TIMEOUT and len(self.recv_window) == 0:
                self.kal_lock.acquire()
                try:
                    # increment kal count value for every kal packet sent
                    self.kal_count = self.kal_count + 1
                finally:
                    self.kal_lock.release()
                print("The kal count is", self.kal_count)
                if self.kal_count >= 2:  # threshold value
                    return

                else:
                    packet = Packet(
                        control_bits={"SYN": 0, "ACK": 0, "ACKNUM": 0, "FIN": 0, "CHK": 0, "KAL": 1, "NAK": 0},
                        seqNum=0,
                        data="",
                    )
                    self.write_to_sock(packet)


    def connect_sock(self, hostname, port):
        self.sock.connect((hostname, port))
        self.is_connected = True
        print("Connected")

    def get_next_seq(self):
        self.seq_num_lock.acquire()
        try:
            self.curr_seq = self.curr_seq + 1
        finally:
            self.seq_num_lock.release()
        print("Seq num", self.curr_seq)
        return self.curr_seq

    def disconnect(self):
        print("The connection is being closed...")
        self.is_connected = False
        self.expiry_timestamp = time.time()
        self.listening_thread.join()
        print("Listening thread closed")
        self.retransmission_thread.join()
        print("Retransmission thread closed")
        self.kal_thread.join()
        print("Kal thread closed")
        self.sock.close()
        sys.exit()

    def listen(self):
        if self.is_connected == False:
            raise Exception("Peer not connected")

        self.listening_thread = Thread(target=self.listen_helper)
        self.retransmission_thread = Thread(target=self.retransmit)
        self.kal_thread = Thread(target=self.keep_alive)

        self.listening_thread.start()
        self.retransmission_thread.start()
        self.kal_thread.start()
       

    def establish_conn(self):
        packet = Packet(
                        control_bits={"SYN": 1, "ACK": 0, "ACKNUM": self.curr_seq, "FIN": 0, "CHK": 1, "KAL": 0, "NAK": 0},
                        seqNum=self.curr_seq,
                        data="",
                    )
        self.write_to_sock(packet)
        print("Sent Syn")
        pass
    
    def listen_helper(self):
        
        if self.sock == None:
            raise Exception("Socket not created")

        ack_count = 0
        ack_map = set()

        print("Listening... ")
        while True:
            if self.is_connected == False:
                break
            self.receive_lock.acquire()
            try:
                data, addr = self.sock.recvfrom(self.BUFFSZ)
            except Exception as _:
                return
            finally:
                self.receive_lock.release()
            data_received = data
            data_received = pickle.loads(data_received)
            # updates the latest packet time for use in the keep-alive fx
            self.latest_packet_time = time.time()

            print("Inside RUDP : Currently received :", data_received["seqNum"])  # printing the data received
            if data_received["SYN"]==1:
                if data_received["ACK"]==1:
                   print("Received SYN-ACK packet, Established connection")
                   self.is_conn_est = True
                else:
                    print("Received SYN packet")

            if data_received["ACK"] == 1 and data_received["SYN"]==0:
                self.kal_lock.acquire()
                try:
                    self.kal_count = 0  # set kal_count because packet is not a KAL packet
                finally:
                    self.kal_lock.release()
                print("received ACK for : ", data_received["seqNum"])
                if(data_received["seqNum"] == 0):
                    print("Establshed Connection")
                    self.is_conn_est = True
                print("# packets in buffer: ", len(self.send_window))
                ack_count += 1
                ack_map.add(data_received["ACKNUM"])
                if ack_count >= (0):

                    ack_count = 0
                    temp_sent_buffer = []
                    self.transmit_lock.acquire()
                    try:
                        for send_window_item in self.send_window:    
                            if send_window_item["packet"].seqNum not in ack_map:
                                temp_sent_buffer.append(send_window_item)
                        self.send_window = temp_sent_buffer
                        ack_map = set()
                    finally:
                        self.transmit_lock.release()
            elif data_received["NAK"] == 1:
                print("Received NAK", data_received["ACKNUM"])
                self.kal_lock.acquire()
                try:
                    self.kal_count = 0  # set kal_count because packet is not a KAL packet
                finally:
                    self.kal_lock.release()
                for send_window_item in self.send_window:
                    if send_window_item["packet"].seqNum == data_received["seqNum"]:
                        self.write_to_sock(send_window_item["packet"], is_retransmit=True)
                        continue
            elif data_received["KAL"] == 1:
                continue
            
            else:
                self.kal_lock.acquire()
                try:
                    self.kal_count = 0  # set kal_count because packet is not a KAL packet
                finally:
                    self.kal_lock.release()

                if data_received["seqNum"] >= (self.delivery_seq + (0.9 * self.WINDOWSZ)):
                    continue
                data_hash = data_received["checksum"]
                data_val = data_received["data"]
                data_hash2 = hashlib.md5(pickle.dumps(data_val)).hexdigest()
                if data_hash != data_hash2:
                    s = data_received["seqNum"]
                    packet = Packet(
                        control_bits={"SYN": 0, "ACK": 0, "ACKNUM": s, "FIN": 0, "CHK": 0, "KAL": 0, "NAK": 1},
                        seqNum=s,
                        data="",
                    )
                    self.write_to_sock(packet)
                    print("Inconsistent data")
                    continue
                if ((len(self.recv_window) < self.WINDOWSZ) or self.recv_map.get(data_received["seqNum"]) != None):
                    s = data_received["seqNum"]
                    packet = Packet(
                        control_bits={"SYN": 1 if (data_received["SYN"] == 1 and data_received["ACK"] == 0) else 0, "ACK": 1, "ACKNUM": s, "FIN": 0, "CHK": 1 if (data_received["SYN"] == 1 and data_received["ACK"] == 0) else 0, "KAL": 0, "NAK": 0},
                        seqNum=s,
                        data="",
                    )
                    self.write_to_sock(packet)

                if len(self.recv_window) < self.WINDOWSZ and self.recv_map.get(data_received["seqNum"]) == None:
                    self.recv_window.append((data_received["seqNum"], data_received))
                    self.recv_map[data_received["seqNum"]] = True

                else:
                    print("data rejected: data already recieved or buffer full")

    def read_from_sock(self):
        if len(self.recv_window) > 0:
            data = min(self.recv_window)
            if data[0] == self.delivery_seq or data[0] == 0:
                print("packet to application: ", data[0])
                if(data[0]!=0):
                    with self.delivery_seq_lock:
                        self.delivery_seq += 1
                self.recv_window.remove(data)
                if(data[0] == 0):
                    print("reading from sock")
                    return None
                else:
                    return data[1]
            else:
                return None
        else:
            return None

    def recv(self):
        while True:
            if self.is_connected == False:
                break
            data = self.read_from_sock()
            if data != None:
                data = deepcopy(data)
                return data
            time.sleep(self.BLOCKING_TIME)

    def write_to_sock(self, packet, is_retransmit=False):

        send_window_item = {
            "packet": packet,
            "time": time.time(),
        }

        if not is_retransmit:
            self.transmit_lock.acquire()  # lock for the send window buffer
            try:
                # if packet contains data, only then append to send window
                if send_window_item["packet"].CHK == 1:
                    self.send_window.append(send_window_item)
            finally:
                self.transmit_lock.release()

        serialized_packet = packet.serialize_packet()
        self.send_lock.acquire()
        try:
            self.sock.sendall(serialized_packet)
        finally:
            self.send_lock.release()


    def send(self, data, control_bits={"SYN": 0, "ACK": 0, "ACKNUM": 0, "FIN": 0, "CHK": 1, "KAL": 0, "NAK": 0}):
        while True:
            if self.is_connected == False:
                return False
            if len(self.send_window) < self.WINDOWSZ:
                break
            else:
                print("Receive window is full")
                time.sleep(self.BLOCKING_TIME)

        seq = self.get_next_seq()
        # dont change packet if user modifies
        data_copy = deepcopy(data)
        packet = Packet(data=data_copy, control_bits=control_bits, seqNum=seq)
        self.write_to_sock(packet)
        return True
