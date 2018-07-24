# Echo client program
import socket
import time
HOST = "192.168.1.10" # The remote PC host
PORT = 30002 # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send ("set_digital_out(0,True)" + "\n") # Set DO_2 = 1
time.sleep(3)
s.send ("set_digital_out(0,False)" + "\n") # Set DO_2 = 0
time.sleep(0.02)
s.send ("set_digital_out(1,True)" + "\n") # Set DO_1 = 1
time.sleep(0.02)
#s.send ("RG2(100)" + "\n")

data1 = s.recv(1024) # Get data from UR

s.close()

# Display the recieved data
print ("Received", repr(data1))
