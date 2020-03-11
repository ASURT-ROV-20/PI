#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64, String
import pid_controller
import time
import json
import ms5837

rospy.init_node("depth_control")
setpoint = 0
sensor = ms5837.MS5837_30BA()
sensor.init()
sensor_offset = 0.35
pid_depth = pid_controller.PID(kp = 1000, ki = 1000, kd = 800,
                                   wind_up = 0.1, upper_limit = 100, lower_limit = -100)
pid_depth.pause()

def main():
    global pid_depth
    setpoint_publisher = rospy.Publisher("setpoint", Float64, queue_size=5)
    pwm_publisher = rospy.Publisher("control_effort", Float64, queue_size=5)
    state_publisher = rospy.Publisher("state",Float64, queue_size=5)
    
    # sensor_offset = calibrate_sensor(sensor, 20)
    rospy.Subscriber("control_status", String, set_depth)
    flag = True
    while not rospy.is_shutdown(): 
        try :
            if pid_depth.enable :
                sensor.read()
                state = sensor.depth() - sensor_offset
                pwm = - pid_depth.update(setpoint, state)
                pwm = int(pwm)
                pwm_publisher.publish(pwm)
                state_publisher.publish(state)
                setpoint_publisher.publish(setpoint)
                flag = True
                time.sleep(0.05)
            else : 
                if flag : 
                    pwm_publisher.publish(0)
                    flag = False 
                time.sleep(0.01)
        except :
            print("Error in control loop")

def calibrate_sensor(sensor, n):
    cal_const = 0
    for i in range(n):
        sensor.read()
        cal_const += sensor.depth()
        time.sleep(0.05)
    return cal_const / n

pre_z = 0
def set_depth(msg):
    global setpoint
    global pid_depth
    global sensor
    msg = json.loads(msg.data)
    if msg["axis"] == "z" :
        if msg["enabled"] :
            sensor.read()
            setpoint = sensor.depth() - sensor_offset
            time.sleep(0.01)
            pid_depth.start()
        else:
            pid_depth.pause()
if __name__ == "__main__":
    main()
