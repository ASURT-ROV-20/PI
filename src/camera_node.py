#!/usr/bin/env python3

import rospy
import json
from std_msgs.msg import String
from camera import Camera    

def camera_callback(data):
    global camera
    global servo_pub

    msg = json.load(data)
    index = int(msg["index"])  
    action = msg["action"]

    if action == "move":
        servo_msg = { camera[index].info()[0] : msg["angle"] }
        servo_pub.publish(servo_msg)
    elif action == "start":
        camera[index].start()
    elif action == "pause":
        camera[index].pause()
    elif action == "stop":
        camera[index].stop()
    return

if __name__ == "__main__" :
    rospy.init_node("camera")
    rospy.Subscriber("QT", String, camera_callback)
    servo_pub = rospy.Publisher("camera_servo", String, queue_size = 5)     

    host = "192.168.1.4"
    port1 = 5000
    port2 = 5001
    port3 = 5002
    
    camera = []
    camera.append(Camera("Main_Cam", 0, host, port1))
    camera.append(Camera("Back_Cam", 1, host, port2))
    camera.append(Camera("Third_Cam", 3, host, port3))
    
    rospy.spin()

