# This file is used to align the rotation quaternions of input traces
# ReplayAR 2024
#
# Usage: run the script with the first file, second file, and output
# file as arguments in that order, where the second trace will be
# aligned to the first.
#
# 
# aligns file2 rotations to file1
# INPUT FORMAT is     timestamp x y z qx qy qz qw
# OUTPUT FORMAT is    timestamp x y z qx qy qz qw

import argparse
import numpy as np
from scipy.spatial.transform import Rotation as R


def read_pose_file(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split() for line in file.readlines()]
    return data

def quaternion_to_matrix(quat):
    return R.from_quat([quat[0], quat[1], quat[2], quat[3]]).as_matrix()

def apply_rotation_to_quaternion(rot_matrix, quat):
    r = R.from_quat([quat[0], quat[1], quat[2], quat[3]])
    rotated_r = R.from_matrix(rot_matrix) * r
    return rotated_r.as_quat()

def transform_poses(file1, file2, output_file):
    data1 = read_pose_file(file1)
    data2 = read_pose_file(file2)
    
    # Extract the first quaternion from each file
    initial_quat1 = list(map(float, data1[0][4:]))
    initial_quat2 = list(map(float, data2[0][4:]))

    # Compute the rotation matrices
    matrix1 = quaternion_to_matrix(initial_quat1)
    matrix2 = quaternion_to_matrix(initial_quat2)
    
    # Calculate the relative rotation matrix
    relative_rotation = matrix1 @ np.linalg.inv(matrix2)

    # Apply this rotation to all quaternions in the second file and write to the new file
    with open(output_file, 'w') as out_file:
        for line in data2:
            quat = list(map(float, line[4:]))
            rotated_quat = apply_rotation_to_quaternion(relative_rotation, quat)
            out_file.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {rotated_quat[0]} {rotated_quat[1]} {rotated_quat[2]} {rotated_quat[3]}\n")


if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='This script aligns the rotations of the second file to the first file.')
    parser.add_argument('first_file', help='ground truth trajectory (format: timestamp tx ty tz qx qy qz qw)')
    parser.add_argument('second_file', help='estimated trajectory (format: timestamp tx ty tz qx qy qz qw)')
    parser.add_argument('third_file', help='output file (format: x y z)')

    args = parser.parse_args()

    transform_poses(args.first_file, args.second_file, args.third_file)
    '''transform_poses("Case3Tests/updated_version/trace_4/Hololens_Trace4_Formatted.txt",
                    "Case3Tests/updated_version/trace_4/Orbslam_Trace4_Formatted.txt",
                    "Case3Tests/updated_version/trace_4/Orbslam_Trace4_RotFormatted.txt")'''
