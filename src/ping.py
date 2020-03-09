#!/usr/bin/env python3

import rospy,time
from std_msgs.msg import Empty

rospy.init_node("Ping")
confirm = rospy.Publisher("ping", Empty,queue_size=5)
while not rospy.is_shutdown():
    confirm.publish()
    print("ping ..")
    time.sleep(0.1)
