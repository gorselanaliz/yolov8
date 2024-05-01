# Library
import cv2
import time

import random 
import numpy as np

from ultralytics import YOLO

# Predefined variables
confidence_score = 0.5

text_color_b = (0,0,0) # black
text_color_w = (255,255,255) # white
background_color = (0,255,0) # bgr

font = cv2.FONT_HERSHEY_SIMPLEX


total_fps = 0
average_fps = 0
num_of_frame = 0

video_frames = []

# Load model
model = YOLO("models/yolov8n.pt") 
labels = model.names


colors = [[random.randint(0,255) for _ in range(0,3)] for _ in labels]

# Load video
video_path = "inference/test.mp4" 
cap = cv2.VideoCapture(video_path) # for webcam: cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("[INFO].. Width:", width)
print("[INFO].. Height:", height)
print("[INFO].. Total Frames:", total_frames)


while True:
    start = time.time()

    ret, frame = cap.read()
    if ret == False:
        break

    results = model(frame, verbose=False)[0] 
    
    # Bboxes, class_id, score
    boxes = np.array(results.boxes.data.tolist())

    for box in boxes:
        # print("[INFO].. Box:", box)
        x1, y1, x2, y2, score, class_id = box
        x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)

        # print("[INFO].. Box:", x1, y1, x2, y2)
        # print("[INFO].. Class:", class_id)
        # print("[INFO].. Score:", score)

        box_color = colors[class_id]

        if score > confidence_score:
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

            score = score * 100
            class_name = results.names[class_id]

            text = f"{class_name}: %{score:.2f}"

            text_loc = (x1, y1-10)

            labelSize, baseLine = cv2.getTextSize(text, font, 1, 1)
            cv2.rectangle(frame, 
                          (x1, y1 - 10 - labelSize[1]), 
                          (x1 + labelSize[0], int(y1 + baseLine-10)), 
                          box_color, 
                          cv2.FILLED)
            
            cv2.putText(frame, text, (x1, y1-10), font, 1, text_color_w, thickness=1)


    end = time.time()

    num_of_frame += 1
    fps = 1 / (end-start)
    total_fps = total_fps + fps

    average_fps = total_fps / num_of_frame
    avg_fps = float("{:.2f}".format(average_fps))

    cv2.rectangle(frame, (10,2), (280,50), background_color, -1)
    cv2.putText(frame, "FPS: "+str(avg_fps), (20,40), font, 1.5, text_color_b, thickness=3)

    video_frames.append(frame)
    print("(%2d / %2d) Frames Processed" % (num_of_frame, total_frames))

    cv2.imshow("Test", frame)
    if cv2.waitKey(20) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


print("[INFO].. Video is creating.. please wait !")

# Video Writer
save_path = "results/test_vid_res.avi"
writer = cv2.VideoWriter(save_path,
                         cv2.VideoWriter_fourcc(*'XVID'),
                         int(avg_fps),
                         (width,height))


for frame in video_frames:
    writer.write(frame)

writer.release()
print("[INFO].. Video is saved in "+save_path)