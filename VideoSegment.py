import cv2
import os
import uuid
import time

cap = cv2.VideoCapture('sample.mov')

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# total_duration = 15
segment_duration = 2

fps = cap.get(cv2.CAP_PROP_FPS)

# total_frames = int(fps * total_duration)
frames_per_segment = int(fps * segment_duration)
print(f"Frames per segment: {frames_per_segment}")
# print(f"Total frames: {total_frames}")

output_folder = f'video_segments_{uuid.uuid4()}'
os.makedirs(output_folder, exist_ok=True)

frame_count = 0
segment_count = 0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = None
# while frame_count < total_frames:
while True:
    ret, frame = cap.read()
    if not ret: 
        print("Error: Failed to capture frame.")
        break

    if frame_count % frames_per_segment == 0:
        if out is not None:
            out.release()
        segment_filename = os.path.join(output_folder, f'segment_{segment_count}.mp4')
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(segment_filename, fourcc, fps, (frame_width, frame_height))
        segment_count += 1
        print(f"Started new segment: {segment_filename}")

    out.write(frame)
    frame_count += 1

cap.release()
if out is not None:
    out.release()

print(f"Captured and saved {segment_count} video segments in the '{output_folder}' folder.")            
