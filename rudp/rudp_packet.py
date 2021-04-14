'''
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
import hashlib
import pickle 

class Packet :
    def __init__(self,control_bits = {"SYN":0, "ACK":0, "ACKNUM":0,"FIN":0,"CHK":0,"KAL":1}, seqNum=0, data = ""):
            
        self.SYN = control_bits["SYN"]
        self.ACK = control_bits["ACK"]
        self.FIN = control_bits["FIN"]
        self.KAL = control_bits["KAL"]
        self.CHK = control_bits["CHK"]
        self.ACKNUM = control_bits["ACKNUM"]
        self.seqNum = seqNum
        self.data = data
        self.checksum = hashlib.md5(pickle.dumps(data)).hexdigest()

    def serialize_packet(self):
        obj = {
            "SYN" :self.SYN,
            "ACK":self.ACK, 
            "ACKNUM":self.ACKNUM,
            "FIN":self.FIN,
            "CHK":self.CHK,
            "KAL":self.KAL,
            "seqNum" : self.seqNum,
            "data" : self.data,
            "checksum" : self.checksum
        }
        
        return pickle.dumps(obj)