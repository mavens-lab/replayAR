import cv2
import numpy as np
import os
import argparse

def find_initial_offset(video_path1, video_path2, fps2, frame_tolerance):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    max_similarity_global = float('-inf')
    best_global_offset = 0
    
    # Initial comparison to find the best offset
    for frame_index1 in range(frame_tolerance):
        ret1, frame1 = cap1.read()
        if not ret1:
            break
        
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for frame_index2 in range(frame_tolerance):
            ret2, frame2 = cap2.read()
            if not ret2:
                continue
            
            frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            s = np.mean(frame1_gray == frame2_gray)
            
            if s > max_similarity_global:
                max_similarity_global = s
                best_global_offset = frame_index1 - frame_index2
    
    cap1.release()
    cap2.release()

    return best_global_offset 
    
def compare_videos(video_path1, video_path2):
    # Create a directory to save the frames if it doesn't exist
    if not os.path.exists('matching_frames'):
        os.makedirs('matching_frames')

    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)

    if not cap1.isOpened() or not cap2.isOpened():
        print("Error: Could not open one or both videos")
        return

    fps2 = cap2.get(cv2.CAP_PROP_FPS)
    frame_tolerance = int(3.0 * fps2)

    # Find the initial best offset
    best_offset = find_initial_offset(video_path1, video_path2, fps2, frame_tolerance)
    print(best_offset)
    start_frame = max(0, -best_offset)  # Adjust the starting index based on the offset
    frame_index1 = start_frame
    total_similarity = 0
    frame_count = 0

    # Adjust video capture start position
    cap1.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    cap2.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_index1 + best_offset))

    while True:
        
        ret1, frame1 = cap1.read()
        if not ret1:
            break

        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        ret2, frame2 = cap2.read()
        if not ret2:
            break

        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Compute the percentage of matching pixels
        similarity_score = np.mean(frame1_gray == frame2_gray)

        total_similarity += similarity_score * 100
        frame_count += 1

        print(f"Frame {frame_index1} compared with offset frame {frame_index1 + best_offset}, similarity: {similarity_score * 100:.2f}%")

        # Concatenate the two frames side by side
        combined_frame = np.hstack((frame1_gray, frame2_gray))

        # Save the combined image
        combined_image_path = os.path.join('matching_frames', f"combined_frame_{frame_index1}.png")
        cv2.imwrite(combined_image_path, combined_frame)

        frame_index1 += 1

    cap1.release()
    cap2.release()

    # Calculate and print the average similarity
    if frame_count > 0:
        average_similarity = total_similarity / frame_count
        print(f"Average similarity between the videos: {average_similarity:.3f}%")
        return average_similarity
    else:
        print("No frames were compared.")
        return 0
    
if __name__ == "__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='This script combines the average pixel similarity of two videos.')
    parser.add_argument('first_file', help='file 1 (mp4)')
    parser.add_argument('second_file', help='file 2 (mp4)')

    args = parser.parse_args()

    compare_videos(args.first_file, args.second_file)

    # Example of many comparison at once
    # c3t1 = compare_videos("Hololens_Trace4_Updated.mp4",
    #                        "Orbslam_Trace4_Updated.mp4")
    # c3t2 = compare_videos("Hololens_Trace5_Updated.mp4",
    #                        "Orbslam_Trace5_Updated.mp4")
    # c3t3 = compare_videos("Hololens_Trace6_Updated.mp4",
    #                        "Orbslam_Trace6_Updated.mp4")
    # c3t4 = compare_videos("Hololens_Trace7_Updated.mp4",
    #                        "Orbslam_Trace7_Updated.mp4")
    # c3t5 = compare_videos("Hololens_Trace8_Updated.mp4",
    #                        "Orbslam_Trace8_Updated.mp4")

    # print(f"c3t1 {c3t1:.2f}%")
    # print(f"c3t2 {c3t2:.2f}%")
    # print(f"c3t3 {c3t3:.2f}%")
    # print(f"c3t4 {c3t4:.2f}%")
    # print(f"c3t5 {c3t5:.2f}%")