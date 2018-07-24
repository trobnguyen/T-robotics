import urx
import time
import logging
import math


# Variables
l = 0.05
v = 2
a = 1.5
w = True
pi = math.pi
target_1 = [0.07390671968460083, -1.730823818837301, -0.5947330633746546, -2.065232578908102, 1.811202883720398, -0.6700151602374476]
target_2 = [2.2142703533172607, -1.4327648321734827, -0.9077032248126429, -2.334079090748922, 1.1734256744384766, 1.4236810207366943]
target_3 = [0.00782569870352745, -1.404228989277975, -1.1874998251544397, -2.1710227171527308, 1.531609058380127, 0.0386592373251915]
target_4 = [4.793690095539205e-05, -6.024037496388246e-06, -1.187631909047262, -2.1710227171527308, 1.5316210985183716, 0.03858770802617073]

def rob_init():
    rob = urx.Robot("192.168.1.10")
    rob.set_tcp((0, 0, 0.19, 0, 0, 0))
    rob.set_payload(0.65, (0, 0, 0.1))
    rob.set_gravity((0, 0, 9.82))
    rob.set_tool_voltage(24)
    rob.set_digital_out(7, 1)
    return rob
 
if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        UR3 = rob_init()
        #UR3.set_payload(0.65)
        time.sleep(0.2) #leave some time to robot to process the setup

        # Move to target_1
        print "Move the robot to target_1: "
        UR3.movej(target_1, acc=a, vel=v, wait=True)

        print "Tool pose in robot joints: "
        pose_rad = UR3.getj()
        pose_deg = UR3.getj()
        for i in range(6):
            pose_deg[i] = pose_rad[i]*180/pi
            print " ",pose_deg[i]
        time.sleep(0.2)
        print "Current tool pose is: ", UR3.getj()
        print "Current tool position is: ", UR3.get_pos()
        print "Current tool orientation is: ", UR3.get_orientation()
        print "   ", UR3.get_pose()
        print "Move the UR3"

        
        for i in range(1):
            UR3.movej(target_1, acc=a, vel=v, wait=True)
            time.sleep(0.2)
            UR3.movej(target_2, acc=a, vel=v, wait=True)
            time.sleep(0.2)
            UR3.movej(target_3, acc=a, vel=v, wait=True)
            time.sleep(0.2)
            #UR3.movej(target_4, acc=a, vel=v, wait=True)
            #time.sleep(0.2)
        

        time.sleep(0.5)
        #rob.movel(pose, acc=a, vel=v, wait=w)
        #pose[2] -= 0.1
        #rob.movel(pose, acc=a, vel=v, wait=w)    
        UR3.set_digital_out(0, 1)
        time.sleep(0.5)
        UR3.set_digital_out(0, 0)
        UR3.set_digital_out(1, 1)
        V = UR3.get_analog_inputs()
        print V

        UR3.send_program("RG2(100)")

        print "End program"
        
        # Set free drive the UR3 during 10s
        #UR3.set_freedrive(1, timeout=10)

    finally:
        UR3.close()






