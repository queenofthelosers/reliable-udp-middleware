import socket
import pickle
import time
import random
import builtins
import hashlib
from copy import deepcopy
from collections.abc import Hashable
from threading import Thread, Lock


class RUDP:
    def _init_(self, hostname, port):
        self.hostname = hostname
        self.port = port
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
        self.transmit_lock = Lock()

    def initialize_socket(self, hostname, port):
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
                    for pkt in self.send_window:
                        elapsed_time = time.time() - pkt["time"]

                        if elapsed_time >= self.TIMEOUT:
                            print("Retransmitting: ", pkt["packet"]["seq"])
                            self.write_to_sock(pkt["packet"], is_retransmit=True)
                finally:
                    self.transmit_lock.release()

    def connect_sock(self, hostname, port):
        pass

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

    def send(self, packet):
        pass
