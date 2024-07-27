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
        print("ERROR: Could not open one or both videos")
        return

    total_iou = 0
    frame_count = 0

    while True:
        ret1, frame1 = cap1.read()
        if not ret1:
            break

        ret2, frame2 = cap2.read()
        if not ret2:
            break

        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # threshold images for non-black pixels
        _, frame1_bin = cv2.threshold(frame1_gray, 1, 255, cv2.THRESH_BINARY)
        _, frame2_bin = cv2.threshold(frame2_gray, 1, 255, cv2.THRESH_BINARY)

        # intersection and union
        intersection = cv2.bitwise_and(frame1_bin, frame2_bin)
        union = cv2.bitwise_or(frame1_bin, frame2_bin)

        # Calculate IoU
        if np.sum(union) != 0:
            iou_score = np.sum(intersection) / np.sum(union)
            total_iou += iou_score
            frame_count += 1
            print(f"Frame {frame_count}, IoU: {iou_score:.2f}")


        # Save the combined image
        combined_image_path = os.path.join('matching_frames', f"combined_frame_{frame_count}.png")
        cv2.imwrite(combined_image_path, np.hstack((frame1_gray, frame2_gray)))

    cap1.release()
    cap2.release()

    # Calculate and print the average IoU
    if frame_count > 0:
        average_iou = total_iou / frame_count
        print(f"Average IoU between the videos: {average_iou:.2f}")
        return average_iou
    else:
        print("No frames were compared.")
        return 0
    
    

if __name__ == "__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='This script combines the average non-black IoU of two videos.')
    parser.add_argument('first_file', help='file 1 (mp4)')
    parser.add_argument('second_file', help='file 2 (mp4)')

    args = parser.parse_args()

    compare_videos(args.first_file, args.second_file)

    # Example of many comparison at once
    # c3t1 = compare_videos("C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Hololens_Trace4_Updated (online-video-cutter.com).mp4",
    #                        "C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Orbslam_Trace4_Updated (online-video-cutter.com).mp4")
    # c3t2 = compare_videos("C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Hololens_Trace5_Updated (online-video-cutter.com).mp4",
    #                        "C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Orbslam_Trace5_Updated (online-video-cutter.com).mp4")
    # c3t3 = compare_videos("C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Hololens_Trace6_Updated (online-video-cutter.com).mp4",
    #                        "C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Orbslam_Trace6_Updated (online-video-cutter.com).mp4")
    # c3t4 = compare_videos("C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Hololens_Trace7_Updated (online-video-cutter.com).mp4",
    #                        "C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Orbslam_Trace7_Updated (online-video-cutter.com).mp4")
    # c3t5 = compare_videos("C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Hololens_Trace8_Updated (online-video-cutter.com).mp4",
    #                        "C:/Users/cshu/Documents/shool_work/2023-2024/holo_remoting_scripts/Case3Tests/updated_version/Orbslam_Trace8_Updated (online-video-cutter.com).mp4")

    # print(f"c3t1 {c3t1:.2f}%")
    # print(f"c3t2 {c3t2:.2f}%")
    # print(f"c3t3 {c3t3:.2f}%")
    # print(f"c3t4 {c3t4:.2f}%")
    # print(f"c3t5 {c3t5:.2f}%")