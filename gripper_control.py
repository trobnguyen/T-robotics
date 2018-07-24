# Echo client program
##########################################################
## Developer: trobnguyen
## Date: 2018-07-20
## Description: 
##
##



import socket
import time

HOST = "192.168.1.20" # The remote host - PCip
PORT = 30000 # The same port as used by the server (can use port 30000, 30001, 30002, 30003, 30004)
BUFFER_SIZE = 1024

print "Starting Program"
count = 0 # number of repeatation

# Create the connection with UR robot by tcp socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) # Bind to the port 
s.listen(1) # Now wait for client connection.
c, addr = s.accept() # Establish connection with client.

print 'Connection address:', addr

# Start loop of sending and receiving data 
while (count < 10):
    try:
        msg = c.recv(1024) # try to get the message from the UR robot
        #print msg
        time.sleep(0.2)
        if msg == "ready": # check the message sent from the UR robot
            input_num = input("0 or 1? ") # input the variable to the UR robot
            count = count + 1 
            print "The count is:", count  
            if input_num == 0:
                data_sent = '0'
                c.send(data_sent.encode('utf8'))
                c.send("(0)") # gripper close
                data = c.recv(BUFFER_SIZE)
                input_num = 1
                print "close gripper"
            else:    
                data_sent = '1' 
                c.send(data_sent.encode('utf8'))
                c.send("(1)") # gripper open
                data = c.recv(BUFFER_SIZE)
                input_num = 0     
                print "open gripper" 
    except socket.error as socketerror:
        print count
    print "received data:", data
    
# close the socket connection
c.close()
s.close()

print "Program finish"
