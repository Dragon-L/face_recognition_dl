import cv2
from face_recognition import face_recognition


video_capture = cv2.VideoCapture(0)
while True:
    _, frame = video_capture.read()
    frame = face_recognition(frame)
    cv2.imshow('name', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()