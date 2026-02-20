#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time

TOPIC = "/jetauto_controller/cmd_vel"

def publish_for(pub, vx=0.0, vy=0.0, wz=0.0, duration=1.0, hz=20):
    msg = Twist()
    msg.linear.x = vx
    msg.linear.y = vy
    msg.angular.z = wz

    rate = rospy.Rate(hz)
    end = time.time() + duration
    while not rospy.is_shutdown() and time.time() < end:
        pub.publish(msg)
        rate.sleep()

    pub.publish(Twist())
    rospy.sleep(0.2)

def run_square(pub):
    publish_for(pub, vx=0.2, duration=5.0)        # forward
    publish_for(pub, vy=0.2, duration=5.0)        # left
    publish_for(pub, wz=-0.6, duration=2.7)       # turn
    publish_for(pub, vy=-0.2, duration=5.0)       # right
    publish_for(pub, vx=0.2, wz=-0.6, duration=5.0)  # forward + turn

if __name__ == "__main__":
    rospy.init_node("jetauto_control")
    pub = rospy.Publisher(TOPIC, Twist, queue_size=10)
    rospy.sleep(1.0)

    input("Press ENTER to start (repeat twice)...")

    for _ in range(2):
        run_square(pub)

    print("Done.")
