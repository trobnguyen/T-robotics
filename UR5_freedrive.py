"""
Date: 2018-07
Author: NGUYEN CANH TOAN
Program: Freedrive teach the UR robot and the robot repeats the taught trajectory
Python version: 3.6.6 64bit
Description: running freedrive teach UR robot with more than 340 teaching targets and can stop teaching before finishing predefined teaching targets
"""

import urx
import time
import logging
import math
import threading
import glob, os                         # for changing file extension
import timeit

# Variables
l = 0.05
r = 0.01                                # blending radius in movel
v = 1.5                                   # velocity
a = 1.5                                   # accelerate
w = True
pi = math.pi

input_timeout = 1000

pre_target = [0, 0, 0, 0, 0, 0]         # previous target
post_target = [0, 0, 0, 0, 0, 0]        # later target

array_target = []                       # array of target points in UR joints coordinate
array_target_l = []                     # array of target points in UR Cartesian coordinate
array_target_l_backup = []              # backup array of target points in UR Cartesian coordinate


sampling_time = 0.001                   # interval between two times of getting new targets
folder = '/media/conanttld/DATA/T_Robotics/Code/GitHub/UR-robots'   # path to the .txt file
start_time = 0
stop_time = 0

home = [0.789987,-2.186899,-0.989705,-1.479532,1.746387,0.211092]   # home position

def rob_init():
    rob = urx.Robot("1.1.1.10")         # connect with the robot ip
    rob.set_tcp((0, 0, 0.19, 0, 0, 0))  # set TCP position
    rob.set_payload(0.65, (0, 0, 0.1))  # set payload and load position
    rob.set_gravity((0, 0, 9.82))       # set gravity
    rob.set_tool_voltage(24)            # set tool voltage
    rob.set_digital_out(7, 1)           # set digital output number 7 to ON
    return rob

def teach_process(arg):
    threading1 = threading.currentThread()
    print('start teach process: ')
    count = 0
    #num_teach_points = 400                  # number of teaching targets
    check_points_1 = 0                      # 1st distance varaiable 
    check_points_2 = 0                      # 2nd distance varaiable
    current_target = [0, 0, 0, 0, 0, 0]     # current target

    current_target = UR5.getj()

    # loop until count > num_teach_points and do_run = False
    while (count < num_teach_points) and getattr(threading1, "do_run", True):   # max count = 340: to use movels command for smooth moving
        # get pre target
        pre_target = UR5.getj()
        pre_target_l = UR5.getl()
        #print "pre_target: ", pre_target
        time.sleep(0.001)

        # get post target
        post_target = UR5.getj()
        post_target_l = UR5.getl()
        #print "post_target: ", post_target
        time.sleep(0.001)
        
        # check distance between two targets are same
        for i in range(6):
            check_points_1 = (pre_target[i] - post_target[i])*(pre_target[i] - post_target[i]) + check_points_1
            

        # if distance <= 10e-6 than pre and post targets are same, this mean ome target is created
        if check_points_1 <= 0.000001:
            
            # check to not save a same target many time comparing current_target and pre_target
            for i in range(6):
                check_points_2 = (pre_target[i] - current_target[i])*(pre_target[i] - current_target[i]) + check_points_2     
                        
            # if current_target != pre_target than a new target will be created
            if check_points_2 >= 0.01:
                current_target = post_target                        # get new current_target
                current_target_l = post_target_l
                
                #stop_time = time.time()
                                
                # write UR script codes into file free_drive.txt
                f.write('movel(p[')                                     
                f.write(",".join(str(bit) for bit in current_target_l)) # convert current_target_l to string with comma between values
                f.write('], a=1.5, v=2, r=0.01)\n')                 # \n for enter new line in text file
                
                array_target.append(current_target)                 # adding more current_target point to the array_target
                array_target_l.append(current_target_l)             # adding more current_target_l point to the array_target_l
                array_target_l_backup.append(current_target_l)      # backup the array_target_l
                count = count + 1                                   # count number of target obtained
                print ('Current tool pose is: ', current_target)
                print ('count:                ', count)
                time.sleep(sampling_time)                           # sampling time
                
                #print ('stop_time - start_time= ',stop_time - start_time,'\n')
                #start_time = stop_time
                
                check_points_2 = 0                                      # reset check_point_2 value for next calculation
        else:
            check_points_1 = 0                                      # reset check_point_1 value for next calculation
    # Close the .txt file
    f.close() 
    if getattr(threading1, "do_run", True):
        print ('Press Enter for moving the UR. ')
         
    
    
if __name__ == "__main__":
    try:
        #logging.basicConfig(level=logging.INFO)
        UR5 = rob_init()  
        time.sleep(0.5)
        
        # Getting the home position and moving the robot to home        
        #home = UR5.getj()
        UR5.movej(home, acc=a, vel=v, wait=True)

        #input_timeout = input("Input the timeout (s) value: ")
        # Set free drive the UR3 during 1000s
        UR5.set_freedrive(1, timeout=input_timeout)

        num_teach_points = int(input("Input number of teaching points: ")) 

        #set_free_drive()

        input("Press Enter for teaching the robot. ")

        # Open a file in the same folder
        f = open('free_drive.txt','w')

        # now threading1 runs regardless of user input
        threading1 = threading.Thread(target=teach_process, args=("task",))
        threading1.daemon = True
        threading1.start()

        
        if input("Press 's' and Enter any time during teaching to stop teaching UR. \n") == 's':
            threading1.do_run = False
            threading1.join()
            time.sleep(1)

        
 
        #input("Input any key for moving the robot. ")



        # Changing every .txt files to .script files for running the program on UR Polyscope
        for filename in glob.iglob(os.path.join(folder, '*.txt')):
            os.rename(filename, filename[:-4] + '.script')          

        # print taught targets
        #print ('taught targets: ', array_target)
        # print number of targets
        target_num = len(array_target_l_backup)
        print ('Number of trained targets: ',target_num)     
       
        # create a temporary array for saving 340 points of the array_target_l
        array_target_temp = []       
        count = 0
        i = 0
        while count < target_num:         
            if count < 339:
                #print ('print count+340*i: ', count+339*i)
                array_target_temp.append(array_target_l[count+339*i])
                array_target_l_backup.remove(array_target_temp[count])
                count += 1
            else:
                #print ('print count: ', count)
                UR5.movels(array_target_temp, acc=a, vel=v, radius=r, wait=True, threshold=None)
                #print ('print array_target_temp: ', array_target_temp)

                array_target_temp = []
                #print ('print array_target_temp: ', array_target_temp)
                count = 0
                i = i + 1
                #print ('print array_target_l_backup: ', array_target_l_backup)
                target_num = len(array_target_l_backup)
                #print ('print len of array_target_l_backup: ', target_num)
        
        # Moving the robot to home
        print ('Move robot to home position')
        UR5.movej(home, acc=a, vel=v, wait=True)
        
        # Move to taught targets
        print ('Move robot to taught targets')
        UR5.movels(array_target_temp, acc=a, vel=v, radius=r, wait=True, threshold=None)

        # Moving to array_target continuously without stop between points       
        #UR5.movels(array_target_l, acc=a, vel=v, radius=0.01, wait=True, threshold=None)

        # Moving the robot to home
        print ('Move robot to home position')
        UR5.movej(home, acc=a, vel=v, wait=True)

        """
        # move point to point with stop between points
        count = 0
        for i in range(target_num):
            UR5.movej(array_target[i], acc=a, vel=v, wait=True)
            #time.sleep(0.2)
            count = count + 1
            print count
        # Moving the robot to home
        UR5.movej(home, acc=a, vel=v, wait=True)
        """

        print ('Current tool pose is: ', UR5.getj())
        print ('End program')

    finally:
        UR5.close()