import math
import json
from enum import Enum
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray

if __name__ == '__main__':
    main()

def main():
    movement = Movement()
    # rospy rate?
    # rospy queue size?

    # subscribe to x, y, r from qt
    qt_sub = rospy.Subscriber("to_be_named_qt", Float32MultiArray, movement.qt_sub_callback)
    equation_pub = rospy.Publisher("Equations",String, queue_size=10)
    while True:
        equation_pub.publish(json.dumps(movement.motors))


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
        self.rotation_efficiency = 0
    
    def qt_sub_callback(self, float_array):
            x, y, r = float_array.data  # todo does that work ?
            self.__horizontal_motors_pwm(x, y, r)

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

        self.motors[MotorPlacement.left_front.value] = round((1 - c) * r_cos_coeff * 100 + c * r * 100, 0)
        self.motors[MotorPlacement.right_front.value] = round((1 - c) * r_sin_coeff * 100 - c * r * 100, 0)
        self.motors[MotorPlacement.right_back.value] = round((1 - c) * r_cos_coeff * 100 - c * r * 100, 0)
        self.motors[MotorPlacement.left_back.value] = round((1 - c) * r_sin_coeff * 100 + c * r * 100, 0)

