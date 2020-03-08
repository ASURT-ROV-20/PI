#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64, String
import pid_controller
import time
import ms5837

def calibrate_sensor(sensor, n):
    cal_const = 0
    for i in range(n):
        sensor.read()
        cal_const += sensor.depth()
        time.sleep(0.1)
    return cal_const / n

def set_depth(msg):
    global setpoint
    global pid_depth
    if msg.data == "set":
        sensor.read()
        setpoint = sensor.depth() - calibration_const
    elif msg.data == "true" :
        pid_depth.enable = True
    elif msg.data == "false" :
        pid_depth.enable = False


rospy.init_node("depth_control")
setpoint_publisher = rospy.Publisher("setpoint", Float64, queue_size=5)
pwm_publisher = rospy.Publisher("control_effort", Float64, queue_size=5)
state_publisher = rospy.Publisher("state",Float64, queue_size=5)

sensor = ms5837.MS5837_30BA()
sensor.init()
calibration_const = calibrate_sensor(sensor, 20)

offset = 340
setpoint = 0

pid_depth = pid_controller.PID(kp = 1000, ki = 1000, kd = 800,
                            wind_up = 20, upper_limit = 100, lower_limit = -100)
pid_depth.enable = True

rospy.Subscriber("QT", String, set_depth)

while not rospy.is_shutdown(): 
    if pid_depth.enable :
        print("Depth is enabled")
        sensor.read()
        state = sensor.depth() - calibration_const
        pwm = - pid_depth.update(setpoint, state)
        pwm += offset
        pwm_publisher.publish(pwm)
        state_publisher.publish(state)
        setpoint_publisher.publish(setpoint)
        time.sleep(0.09)
    else : 
        print("not enabled")
        time.sleep(0.01)


