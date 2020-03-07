#!/usr/bin/env python3

import busio
from Adafruit_PCA9685 import PCA9685
import rospy
from std_msgs.msg import String
import time
import json

devices = {}
cameras = {}

Zero_thruster = 340
Zero_Servo = 225
i2c_bus = busio.I2C(3, 2)			
hat = PCA9685()
hat.set_pwm_freq(50)
delay = 0.000020

def add_Device(name,channel,zero_value):
    devices[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}\
def add_Camera(name,channel,zero_value):
    cameras[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}

def updateMotorPWM(pwms_json):
    pwms = json.loads(pwms_json.data)
    for key in pwms.keys():
        devices[key]['current'] = pwms[key]
    for key in devices.keys():
#        hat.set_pwm(devices[key]['channel'],0,int(devices[key]['current'] + 340))
        if True:
            print(key, devices[key]['channel'],devices[key]['zero'],devices[key]['current']+devices[key]['zero'])
            hat.set_pwm(devices[key]['channel'],0,int(devices[key]['current'] + devices[key]['zero']))
        time.sleep(delay)

def updateCameraPWM(pwms_json):
    pwms = json.loads(pwms_json.data)
    for key in pwms.keys():
        cameras[key]['current'] = pwms[key]
    for key in cameras.keys():
#        hat.set_pwm(devices[key]['channel'],0,int(devices[key]['current'] + 340))
        if True:
            print(key, cameras[key]['channel'],cameras[key]['zero'],cameras[key]['current']+cameras[key]['zero'])
            hat.set_pwm(cameras[key]['channel'],0,int(cameras[key]['current'] + cameras[key]['zero']))
        time.sleep(delay)

def updateSinglePWM(name,current):
    devices[name]['current'] = current
    hat.set_pwm(devices[name]['channel'],devices[name]['zero'],devices[name]['current'])

    time.sleep(delay)

#def PID_Control(pwm_z):
#         pwm = pwm_z.data
#         if abs ( devices['Vertical_Left']['current'] - pwm ) <= 2 or (devices['Vertical_Right']['current'] - pwm ) <= 2:
#                 return
# 
# 
#         time.sleep(delay)
# 
#         devices['Vertical_Left']['current'] =pwm
#         devices['Vertical_Right']['current'] =pwm
#         print("control value:: ",pwm)

def main():
    add_Device('Left_Front', 14, Zero_thruster)
    add_Device('Right_Front', 15, Zero_thruster)
    add_Device('Right_Back', 11, Zero_thruster)
    add_Device('Left_Back', 10, Zero_thruster)
    add_Device('Vertical_Right', 13, Zero_thruster)
    add_Device('Vertical_Left', 12, Zero_thruster)
    add_Camera('cam1',2,Zero_Servo)
    add_Camera('cam2',1,Zero_Servo)
    add_Camera('cam3',99,Zero_Servo) # todo set correct channel

    rospy.init_node('Hardware')
    rospy.Subscriber('Equations',String,updateMotorPWM)
    rospy.Subscriber('Servos',String,updateCameraPWM)
    #rospy.Subscriber("Control",Float64,PID_Control)

    rospy.spin()


main()
