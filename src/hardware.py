#!/usr/bin/env python3

#import busio
from Adafruit_PCA9685 import PCA9685
import rospy
from std_msgs.msg import String,Float64
import time
import json
import math
motors = {}
cameras = {}

Zero_thruster = 340
Zero_Servo = 225
#i2c_bus = busio.I2C(3, 2)
hat = PCA9685()
hat.set_pwm_freq(50)
delay = 0.000020
control_pwm = 0


def add_Motor(name,channel,zero_value):
    motors[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}

def add_Camera(name,channel,zero_value):
    cameras[name] = {'channel':channel , 'zero':zero_value , 'current': zero_value}

def updateMotorPWM(pwms_json):
	pwms = json.loads(pwms_json.data)
	for key in pwms.keys():
		motors[key]['current'] = pwms[key]
	current_z = motors["Vertical_Left"]["current"]
	motors["Vertical_Left"]["current"] = current_z if current_z else control_pwm
	motors["Vertical_Right"]["current"] = motors["Vertical_Left"]["current"]
	for key in motors.keys():
		current_pwm = motors[key]['current']
		if not math.isnan(current_pwm):
		    print(key, motors[key]['channel'],int(current_pwm+motors[key]['zero']))
		    hat.set_pwm(motors[key]['channel'],0,int(current_pwm + motors[key]['zero']))
		time.sleep(delay)

def updateCameraPWM(pwms_json):
	pwms = json.loads(pwms_json.data)
	for key in pwms.keys():
		cameras[key]['current'] = pwms[key]
	for key in cameras.keys():
		current_pwm = cameras[key]['current']
		if not math.isnan(current_pwm):
		    print(key, cameras[key]['channel'],int(current_pwm))
		    hat.set_pwm(cameras[key]['channel'],0,int(current_pwm + cameras[key]['zero']))
		time.sleep(delay)


def updateSinglePWM(name,current):
    motors[name]['current'] = current
    hat.set_pwm(motors[name]['channel'],motors[name]['zero'],motors[name]['current'])

    time.sleep(delay)

def addHardwareDevices():
	add_Motor('Left_Front', 14, Zero_thruster)
	add_Motor('Right_Front', 15, Zero_thruster)
	add_Motor('Right_Back', 11, Zero_thruster)
	add_Motor('Left_Back', 10, Zero_thruster)
	add_Motor('Vertical_Right', 13, Zero_thruster)
	add_Motor('Vertical_Left', 12, Zero_thruster)
	add_Camera('cam1',1,Zero_Servo)
	add_Camera('cam2',0,Zero_Servo)
	add_Camera('cam3',2,Zero_Servo)

def pid_callback(pwm_z):
	global control_pwm
	control_pwm = pwm_z.data

def main():

    addHardwareDevices()
    rospy.init_node('Hardware')
    rospy.Subscriber('Equations',String,updateMotorPWM)
#    rospy.Subscriber('Servos',String,updateCameraPWM)
    rospy.Subscriber('control_effort',Float64,pid_callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
