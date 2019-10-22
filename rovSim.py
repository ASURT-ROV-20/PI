#!/usr/bin/env python3

import rospy,time,threading,sys
from std_msgs.msg import Empty

connected = True

def checkPing():
    while(True):
        global connected
        if(connected):
            connected = False
        else :
            print("Disconnected !!!!!")
            sys.exit(1)
        time.sleep(0.15)


def pingCallback(data):
    global connected
    connected = True
    print("ping .....")


rospy.init_node("rovSim")
my_sub = rospy.Subscriber("ping", Empty,pingCallback)
threading.Thread(target=checkPing,args=[]).start()
rospy.spin()
