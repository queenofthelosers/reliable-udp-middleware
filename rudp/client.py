from rudp_protocol import RUDP

r = RUDP("127.0.0.1",9001,False)
r.connect_sock("127.0.0.1",9002)
r.listen()
r.send("this is a message")
