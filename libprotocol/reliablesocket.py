import socket
import pickle 

class ReliableSocket:
    def __init__(self, sock=None,ip="127.0.0.1",port=20001, timeout = 5):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((ip,port))
            self.sock.settimeout(timeout)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def reliableSend(self, payload,address):
        payload = pickle.dumps(payload)
        self.sock.sendto(payload, address)
        # totalsent = 0
        # while totalsent < MSGLEN:
        #     sent = self.sock.send(msg[totalsent:])
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     totalsent = totalsent + sent

    def reliableReceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)