import numpy as np
from scipy.spatial.transform import Rotation as R

# aligns file2 rotations to file1
# INPUT FORMAT is     timestamp x y z qx qy qz qw
# OUTPUT FORMAT is    timestamp x y z qx qy qz qw

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

# Example usage:
transform_poses("Case2Tests/trace_5/MH05_GT_Formatted.txt",
                "Case2Tests/trace_5/f_dataset-MH05_stereoi.txt",
                "Case2Tests/trace_5/euroc5_RotAligned.txt")
