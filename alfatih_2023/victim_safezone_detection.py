import numpy as np
import cv2
import math
import time
# Extract Frames
cap = cv2.VideoCapture(0)

hsv_lower = [[0,139,91],
             [62,41,82]]
hsv_upper = [[46,255,255],
             [84,255,255]]
area_lim = [100,100]

# used to record the time when we processed last frame
prev_frame_time = 0
  
# used to record the time at which we processed current frame
new_frame_time = 0

def empty(a):
    pass


# Define object specific variables
dist = 0
focal = [450,
         570]
pixels = 30
width = [12,13.6]
distance_object = 0
mode = 0

def get_dist(rectange_params,mode):
    # find no of pixels covered
    pixels = rectange_params[1][0]
    # print(pixels)
    # calculate distance
    dist = (width[mode]*focal[mode])/pixels

    return dist


# basic constants for opencv Functs
kernel = np.ones((3, 3), 'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX
org = (0, 20)
fontScale = 0.6
color = (0, 0, 255)
thickness = 2

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 300, 550)
cv2.createTrackbar("HUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("HUE Max", "HSV", 46, 255, empty)
cv2.createTrackbar("SAT Min", "HSV", 139, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 91, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
cv2.createTrackbar("Thresh Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Thresh Max", "HSV", 255, 766, empty)
cv2.createTrackbar("Area", "HSV", 100, 1000, empty)


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def object_tracking():
    global mode
    global new_frame_time, prev_frame_time
    global distance_obj
    ret, img = cap.read()

    # Define the new size (width, height)
    new_width = 640
    new_height = 480
    new_size = (new_width, new_height)

    # Resize the frame
    img = cv2.resize(img, new_size)

    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    
    
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    # Threshold
    thresh_min = cv2.getTrackbarPos("Thresh Min", "HSV")
    thresh_max = cv2.getTrackbarPos("Thresh Max", "HSV")

    frame_height, frame_width, _ = img.shape
    # print(frame_height, frame_width)
    center_x = int(frame_width / 2)
    center_y = int(frame_height / 2)
    
    # Area
    area = cv2.getTrackbarPos("Area", "HSV")

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([hsv_lower[mode][0],hsv_lower[mode][1],hsv_lower[mode][2]])
    upper = np.array([hsv_upper[mode][0],hsv_upper[mode][1],hsv_upper[mode][2]])
    mask = cv2.inRange(hsv_img, lower, upper)
    thresh = cv2.threshold(mask, thresh_min, thresh_max,
                           cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=5)
    cont, hei = cv2.findContours(
        d_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:1]

    for cnt in cont:
        # check for contour area
        if (cv2.contourArea(cnt) > 10 and cv2.contourArea(cnt) < 306000):
            
            # Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            pixels = rect[1][0]
            # print(pixels)
            
            if (pixels >= area_lim[mode]):
                x2, y2, w2, h2 = cv2.boundingRect(cnt)
                cx = int(x2 + w2/2)
                cy = int(y2 + h2/2)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)
                cv2.circle(img, (center_x, center_y), 5, (255, 255, 0), -1)
                cv2.circle(img, (center_x, cy), 5, (0, 255, 0), -1)
                cv2.circle(img, (center_x, frame_height), 5, (0, 255, 0), -1)
                koordinat = np.array([cx,cy])
                img = cv2.line(img,(int(frame_width/2),int(cy)),(int(frame_width/2), int(frame_height)),(255,0,0))
                img = cv2.line(img,(int(cx),int(cy)),(int(center_x), int(cy)),(255,0,0))
                # img = cv2.line(img,(int(frame_width/2),int(frame_height/2)),(int(frame_width/2), int(frame_height)),(255,0,0))
                img = cv2.line(img,(int(cx),int(cy)),(int(frame_width/2), int(frame_height)),(255,0,0))
                if cx < center_x :
                    dist_x = cx - center_x
                else:
                    dist_x = cx - center_x
                
                dist_y = frame_height - cy
                
                print("dist x : ", dist_x, end="  ", flush=True)
                print("dist y : ", dist_y, end="  ", flush=True)
                
                theta = math.degrees(math.atan2(dist_y,dist_x))
                print("theta : ", theta)
                
                cv2.putText(img, str(koordinat), (cx , cy +30), font,
                            fontScale, color, 1, cv2.LINE_AA)
                cv2.putText(img, str(np.array([center_x,cy])), (center_x+30,cy -20), font,
                            fontScale, color, 1, cv2.LINE_AA)
                cv2.putText(img, str(np.array([center_x,frame_height])), (center_x+30,frame_height -20), font,
                            fontScale, color, 1, cv2.LINE_AA)
                cv2.putText(img, str(np.array(["theta : ",theta])), (center_x - 50,frame_height -50), font,
                            fontScale, color, 1, cv2.LINE_AA)
                
                
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], -1, (255, 0, 0), 3)
                distance_obj = get_dist(rect,mode)
                # Wrtie n the image
                cv2.putText(img, 'Distance from Camera in CM :',
                            org, font,  1, color, 2, cv2.LINE_AA)
                cv2.putText(img, str(distance_obj), (110, 50), font,
                            fontScale, color, 1, cv2.LINE_AA)
                cv2.putText(img, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    img_track = stackImages(1.4, ([img, d_img]))
    cv2.imshow('ImageStack', img_track)


# loop to capture video frames
while True:
    object_tracking()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
