import numpy as np
import argparse

def combine(position_filename, rotation_filename, output_filename):
        
    # Open the input file and read the positions
    with open(position_filename, 'r') as f: #'aligned_positions.txt', 'r') as f:
        positions = [list(map(float, line.split())) for line in f.readlines()[1:]]

    # Convert the positions to a numpy array
    positions = np.array(positions)

    # Open the input file and read the timestamps and quaternions
    with open(rotation_filename, 'r') as f:#'aligned_rotations.txt', 'r') as f:
        lines = [line.split() for line in f.readlines()]
        timestamps = [line[0] for line in lines]
        quaternions = np.array([[float(val) for val in line[4:]] for line in lines])


    # Get the minimum length of the two arrays
    min_len = min(len(positions), len(quaternions))

    # Open the output file and write the timestamps, new positions, and normalized quaternions
    with open(output_filename, 'w') as f:#'normalized_and_combined.txt', 'w') as f:
        for i in range(min_len):
            f.write(timestamps[i] + ' ' + ' '.join(map(str, positions[i])) + ' ' + ' '.join(map(str, quaternions[i])) + '\n')


if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='''
    This script combines the aligned positions and rotations (does no normalization)
    ''')
    parser.add_argument('first_file', help='position file (format: tx ty tz)')
    parser.add_argument('second_file', help='rotation file (format: timestamp tx ty tz qx qy qz qw)')
    parser.add_argument('output_file', help='output file name', default='normalized_and_combined.txt')

    args = parser.parse_args()

    combine(args.first_file, args.second_file, args.output_file)