#!/usr/bin/env python3.7

import busio
from Adafruit_PCA9685 import PCA9685
import rospy
from std_msgs.msg import String
import time
import json

devices = {}
Zero_thruster = 305
Zero_Servo = 225
i2c_bus = busio.I2C(3, 2)			
hat = PCA9685(i2c_bus)
hat.frequency = 50
delay = 0.000020

def add_Device(name,channel,zero_value):
    devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}

def updatePWM(pwms_json):
    pwms = json.loads(pwms_json.data)
    for key in pwms.keys():
        devices[key]['current'] = pwms[key]
    for key in devices.keys():
        #hat.set_pwm(devices[key]['channel'],devices[key]['zero'],devices[key]['current'])
        #hat.channels[devices[key]['channel']].duty_cycle = devices[key]['current']
        rospy.loginfo(devices[key]['channel'],devices[key]['zero'],devices[key]['current'])
        time.sleep(delay)
    


def updateSinglePWM(name,current):
    devices[name]['current'] = current
    #hat.set_pwm(devices[name]['channel'],devices[name]['zero'],devices[name]['current'])
    
    time.sleep(delay)


def main():
    add_Device('Left_Front', 5, Zero_thruster)
    add_Device('Right_Front', 2, Zero_thruster)
    add_Device('Right_Back', 13, Zero_thruster)
    add_Device('Left_Back', 15, Zero_thruster)
    add_Device('Vertical_Right', 9, Zero_thruster)
    add_Device('Vertical_Left', 11, Zero_thruster)
    hat.add_Device('Main_Cam',0,Zero_Servo)
    hat.add_Device('Back_Cam',1,Zero_Servo)

    rospy.init_node('Hardware')
    rospy.Subscriber('Equations',String,updatePWM)
    #rospy.Subscriber("Control",Float64,Control_PID)

    rospy.spin()


main()
