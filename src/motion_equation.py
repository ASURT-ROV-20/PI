#!/usr/bin/env python3

import math
import json
from enum import Enum
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Quaternion


def main():
    rospy.init_node('equation_node', anonymous=True)
    rate = rospy.Rate(10)  # 10hz  # ? rospy rate?
    # rospy.init_node('qt_equation_listener', anonymous=True)
    movement = Movement()

    # subscribe to x, y, z, r from qt .
    # Quaternion sends float64 x, y, z, w where w will correspond to the rotation r
    # ? will both nodes yshta8alo ma3 ba3d kda 3adi? (threading q)
    rospy.Subscriber("rov_velocity", Quaternion, movement.qt_sub_callback)
    equation_pub = rospy.Publisher("Equations",String, queue_size=10)  # ? rospy queue size?
    while not rospy.is_shutdown():
        motion_json = json.dumps(movement.motors)
        equation_pub.publish(motion_json)
        rospy.loginfo(motion_json)
        rate.sleep()


class MotorPlacement(Enum):
    right_front = "Right_Front"
    left_front = "Left_Front"
    right_back = "Right_Back"
    left_back = "Left_Back"
    vertical_right = "Vertical_Right"
    vertical_left = "Vertical_Left"


class Movement:
    def __init__(self):
        self.motors = {motor.value: 0 for motor in MotorPlacement}
        self.rotation_efficiency = 0.2

    def qt_sub_callback(self, msg):
        self.__horizontal_motors_pwm(msg.x, msg.y, msg.w)
        self.__vertical_motors_pwm(msg.z)

    def __vertical_motors_pwm(self, z):
        z_pwm = round(z * 100)
        self.motors[MotorPlacement.vertical_left.value] = z_pwm
        self.motors[MotorPlacement.vertical_right.value] = z_pwm

    def __horizontal_motors_pwm(self, x, y, r):
        """take movement coordinates in the range of [-1, 1]

        :param x: movement in x
        :param y: movement in y
        :param r: rotation (clockwise)
        :return: the four horizontal motors pwm range [0, 100] (int)
        """
        theta = math.atan2(y, x)

        # Reference:
        # https://www.xarg.org/2017/07/how-to-map-a-square-to-a-circle/
        x_circle_coord_squared = x * x * (1 - y * y / 2)
        y_circle_coord_squared = y * y * (1 - x * x / 2)

        resultant = math.sqrt(x_circle_coord_squared + y_circle_coord_squared)
        # ================================================
        # Axis Rotation
        theta -= math.pi / 4

        #  Coefficient
        sin = math.sin(theta)
        cos = math.cos(theta)
        max_sinusoidal = max(abs(sin), abs(cos))
        # ============ ( c ) is the Rotation Efficiency =================
        c = self.rotation_efficiency
        r_cos_coeff = resultant * cos / max_sinusoidal
        r_sin_coeff = resultant * sin / max_sinusoidal

        self.motors[MotorPlacement.left_front.value] = (  r_cos_coeff - r * c )  *100
        self.motors[MotorPlacement.right_front.value] =(   r_sin_coeff +  r * c) *100
        self.motors[MotorPlacement.right_back.value] = (  r_cos_coeff + r * c )  *100
        self.motors[MotorPlacement.left_back.value] =  ( r_sin_coeff -  r * c )  *100


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
