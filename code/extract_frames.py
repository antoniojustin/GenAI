import os
import cv2
import numpy as np


def extract_frames_from_folder(input_folder, output_folder, frames_per_video=5):
    """
    Extract 'frames_per_video' frames from each video in 'input_folder'
    and save them under 'output_folder'.

    For each video, we create a subfolder named after the video file (no extension).
    """
    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a video by extension (you can add more extensions if needed)
        if filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            video_path = os.path.join(input_folder, filename)

            # Create a subfolder for this particular video (exclude the extension from folder name)
            video_name = os.path.splitext(filename)[0]
            video_output_dir = os.path.join(output_folder, video_name)
            os.makedirs(video_output_dir, exist_ok=True)

            # Open the video file with OpenCV
            cap = cv2.VideoCapture(video_path)

            # Get the total number of frames in the video
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # If the video is too short, adjust frames_per_video if needed
            # (for example, if total_frames < frames_per_video, we handle that gracefully)
            frames_to_extract = min(frames_per_video, total_frames)

            # Determine the specific frames we want to sample (evenly spaced)
            frame_indices = np.linspace(0, total_frames - 1, frames_to_extract, dtype=int)

            print(f"Extracting {frames_to_extract} frames from '{filename}' ...")

            for i, frame_index in enumerate(frame_indices):
                # Set the video position to the frame_index
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                ret, frame = cap.read()

                if not ret:
                    # Could not read frame (e.g., if we are near end of file)
                    break

                # Construct output path for this frame
                # e.g., "frames/adults/video_adult1/frame_0.jpg"
                frame_filename = f"frame_{i}.jpg"
                frame_path = os.path.join(video_output_dir, frame_filename)

                # Save the frame as a JPEG file
                cv2.imwrite(frame_path, frame)

            # Release the video capture
            cap.release()


def main():
    # Specify the paths
    adult_videos_folder = "data/Adult"
    child_videos_folder = "data/Children"
    adult_frames_output = "frames/Adult"
    child_frames_output = "frames/Children"

    frames_per_video = 5

    # Extract frames from adult videos
    extract_frames_from_folder(adult_videos_folder, adult_frames_output, frames_per_video)
    # Extract frames from children videos
    extract_frames_from_folder(child_videos_folder, child_frames_output, frames_per_video)

    print("Frame extraction complete!")


if __name__ == "__main__":
    main()