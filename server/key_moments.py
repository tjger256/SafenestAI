import cv2
import os
import argparse

# Supported video file extensions
SUPPORTED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}

def extract_key_frames(video_path, threshold=100, min_contour_area=1000):
    # Check file extension
    _, ext = os.path.splitext(video_path)
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        print(f"Error: Unsupported file type '{ext}'. Supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}")
        return
    
    # Extract the base name of the video file without extension
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Create the output directory based on the video file name
    output_dir = f"{base_name}_output"
    
    # Read the video from specified path
    cam = cv2.VideoCapture(video_path)
    if not cam.isOpened():
        print("Error: Unable to read video")
        return

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Frame counters
    current_frame = 0
    key_frame_count = 0

    # Read the first frame
    ret, prev_frame = cam.read()
    if not ret:
        print("Error: Unable to read video")
        return

    # Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    while True:
        # Read the next frame
        ret, frame = cam.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Compute the absolute difference between the current frame and the previous frame
        frame_diff = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)[1]

        # Dilate the threshold image to fill in holes, then find contours on threshold image
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if there is any significant motion
        motion_detected = any(cv2.contourArea(contour) > min_contour_area for contour in contours)

        if motion_detected:
            # Save the frame in the output directory
            frame_name = os.path.join(output_dir, f'frame{key_frame_count}.jpg')
            print(f'Creating... {frame_name}')
            cv2.imwrite(frame_name, frame)
            key_frame_count += 1

        # Update the previous frame
        prev_gray = gray
        current_frame += 1

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract key frames from a video.')
    parser.add_argument('video_path', type=str, help='Path to the video file')
    parser.add_argument('--threshold', type=int, default=100, help='Threshold for detecting motion')
    parser.add_argument('--min_contour_area', type=int, default=1000, help='Minimum contour area to be considered as motion')
    args = parser.parse_args()

    extract_key_frames(args.video_path, args.threshold, args.min_contour_area)

