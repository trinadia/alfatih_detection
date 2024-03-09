import cv2

# Initialize webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Failed to open webcam.")
    exit()

# Read first frame to get frame size
ret, frame = cap.read()
if not ret:
    print("Error: Failed to read frame.")
    exit()

# Get frame size
height, width = frame.shape[:2]

# Release webcam
cap.release()

# Calculate center point
center_x = width // 2
center_y = height // 2

print("Frame Size: {}x{}".format(width, height))
print("Center Point: ({}, {})".format(center_x, center_y))
