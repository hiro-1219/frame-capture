import cv2

cap = cv2.VideoCapture("./data/IMAG0025.mp4")
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
