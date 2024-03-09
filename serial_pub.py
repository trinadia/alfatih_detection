# import serial
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

# cap.release()
'''

- set port
- serial write to new program (C++/Arduino) to 

'''
# coordinates of setpoint's center
x_cp_sp = width // 2
y_cp_sp = height // 2
area_sp = width * height # setpoint area
x_tol_err = 10 # tolerated x error
y_tol_err = 10 # tolerated y error


class yolo_serial:
    def __init__(self, x1, y1, x2, y2):
        # detect.py: map(int, xyxy)
        # serial.py: def __init__(self, xyxy)
        # x1, y1, x2, y2 = map(int, xyxy)

        # detected centerpoint's coordinates
        x_cp_det = (x2 + x1)/2
        y_cp_det = (y1 + y2)/2

        # calculate position error
        # conditions: if x_detect > x_cp_sp... if necessary
        x_err = x_cp_det - x_cp_sp
        y_err = y_cp_det - y_cp_sp

        self.x = x_cp_det
        self.y = y_cp_det
        '''
        if the bounding box's area is << area_sp:
            approach the target --> send signal to legs
        
        if the bounding box's area approaches area_sp (error+= 5-10 px):
            if x_err >> x_tol_err:
                turn head toward the target --> send signal to head
            elif x_err << x_tol_err:
                ready to grip
        '''

        # self.publish = 
        # usage: yolo_serial(x1, y1, x2, y2).publish

# class color_serial:
    '''
    applicable conditions
    '''