'''
@author: Sarthak Ahuja

Sample Run:
python correct_kinect_transform.py --trans 0.044 0.080 0.619 --euler -0.067 1.103 -0.045

Expected Output:
There you go -
rosrun tf static_transform_publisher 0.044 0.08 0.619 1.63779632679 3.18659265359 0.467796326795 /reference/base /kinect2_link 10
'''

import argparse
import numpy as np

def main(trans, euler):
    '''
    The baxter_kinect_calibration package returns the following when you run "rosrun tf tf_echo /reference/base /kinect2_link"- 
    At time 1557208373.500
    - Translation: [0.097, -0.127, 0.890]
    - Rotation: in Quaternion [-0.017, 0.524, -0.002, 0.852]
                in RPY (radian) [-0.067, 1.103, -0.045]
                in RPY (degree) [-3.864, 63.181, -2.591]
                
    This function returns the command to run the static transform
    '''
    Y = euler[2]
    P = euler[1]
    R = euler[0]
    
    Y_ = (np.pi/2) - R 
    P_ = np.pi - Y
    R_ = (np.pi/2) - P
    
    print("There you go - ")
    print("rosrun tf static_transform_publisher {} {} {} {} {} {} /reference/base /kinect2_link 10".format(trans[0], trans[1], trans[2], Y_, P_, R_))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--euler", nargs="*", type=float, default=[0,0,0], help="euler transform returned to you by baxter_h2r_kinect_calibration - RPY format in radians")
    parser.add_argument("--trans", nargs="*", type=float, default=[0,0,0], help="translation vector")
    args = parser.parse_args()
    main(args.trans, args.euler)