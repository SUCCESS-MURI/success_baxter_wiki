#!/usr/bin/env python

import os
import tf
import rospy
import argparse
import numpy as np

"""
Node for automatically generating commands for publishing the static transform 
between base and kinect frames during calibration
"""

def transform_command(base_frame, kinect_frame, trans, euler):
    '''
    This function returns the command to run the static transform between the base and kinect frames
    '''
    Y = euler[2]
    P = euler[1]
    R = euler[0]

    # in front of baxter
    Y_ = Y - np.pi/2
    P_ = R 
    R_ = -(P + np.pi/2) 
    
    # on baxter
    # Y_ = (np.pi/2) - R 
    # P_ = -(np.pi - Y)
    # R_ = (np.pi/2) - P
    print "<node pkg='tf' type='static_transform_publisher' name='kinect_broadcaster' args='{} {} {} {} {} {} {} {} 10' />".format(trans[0], trans[1], trans[2], Y_, P_, R_, base_frame, kinect_frame)
    return "rosrun tf static_transform_publisher {} {} {} {} {} {} {} {} 10".format(trans[0], trans[1], trans[2], Y_, P_, R_, base_frame, kinect_frame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_frame", help="frame we are grounding kinect frame in", type=str)
    parser.add_argument("kinect_frame", help="name of newly created kinect frame", type=str)
    args = parser.parse_args()
    
    rospy.init_node("kinect_transform", anonymous=True)
    listener = tf.TransformListener()
    try:
        listener.waitForTransform(args.base_frame, args.kinect_frame, rospy.Time(0), rospy.Duration(5.0))
        transform = listener.lookupTransform(args.base_frame, args.kinect_frame, rospy.Time(0))
        trans = transform[0]
        euler = tf.transformations.euler_from_quaternion(transform[1])
        output = transform_command(args.base_frame, args.kinect_frame, trans, euler)
        print output

        response = raw_input("Would you like to run the transform now? ")
        if response in ["y", "Y", "yes", "Yes"]:
            rospy.loginfo("Broadcasting transform between {} and {}".format(args.base_frame, args.kinect_frame))
            os.system(output)
            rospy.loginfo("Exiting transform broadcast...")
        else:
            rospy.loginfo("Broadcast canceled")

    except Exception as e:
        rospy.logerr(e)
    



    
