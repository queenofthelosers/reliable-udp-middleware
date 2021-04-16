import subprocess
from subprocess import Popen, PIPE
import csv , json
import os


# subprocess.call(["g++", "Test.cc"]) # OR gcc for c program
print("hello world")
# server= Popen(['python','rudp/server/server.py'], shell=True, stdout=PIPE, stdin=PIPE)

client = Popen([" python "," client.py "," pic.jpg "], shell=True, stdout=PIPE, stdin=PIPE,cwd="rudp/client")

# value = bytes(value, 'UTF-8')  # Needed in Python 3.
# p.stdin.write(value)
# p.stdin.flush()
output = client.stdout.readline()

print(output)




 
