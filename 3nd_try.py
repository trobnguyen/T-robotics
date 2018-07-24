# Echo client program
import socket
import time

HOST = "192.168.1.20" # The remote host
PORT = 30000 # The same port as used by the server

print "Starting Program"
count = 0
#a = 0

print "checked_1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "checked_2"
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) # Bind to the port 
print "checked_3"

s.listen(1) # Now wait for client connection.
print "checked_4"
c, addr = s.accept() # Establish connection with client.
print "checked_5"
 
while (count < 10):
     
    try:
        msg = c.recv(1024)
        #print msg
        time.sleep(0.5)
        if msg == "ready":
            a = input("0 or 1? ")
            count = count + 1
            print "The count is:", count  
            if a == 0:
                c.send("(0)") # gripper close
                a = 1
                print "close gripper"
            else:    
                c.send("(1)") # gripper open
                a = 0     
                print "open gripper" 
    except socket.error as socketerror:
        print count
    

c.close()
s.close()

print "Program finish"