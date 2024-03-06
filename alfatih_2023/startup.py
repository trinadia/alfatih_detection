# import cv2
# video = cv2.VideoCapture(0)
# # video.set(3,640)
# # video.set(4,480)
# # video.set(10,100)

# while True:
#     success, img = video.read()
#     cv2.imshow("Hasil", img)
#     if cv2.waitKey(1) & 0xFF ==ord('q'):
#         break
# print("Hello")

import cv2
import numpy as np
import os
import time
import serial
import math
import struct
MIN_MATCH_COUNT=40

detector=cv2.ORB_create()
data = []
pTime = 0
cTime = 0

hsv_lower = [[0,139,91],
             [62,41,82]]
hsv_upper = [[46,255,255],
             [84,255,255]]
area_lim = [100,100]

def empty(a):
    pass

# Define object specific variables
dist = 0
focal = [450,
         570]
pixels = 30
width = [12,13.6]
distance_object = 0
mode = 1

path = "/home/alfatih/alfatih_2023/picture"
images = []
classNames = []
myList = os.listdir(path)

ser = serial.Serial(port='/dev/ttyACM0', baudrate=4800, timeout=1)

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

def get_dist(rectange_params,mode):
    # find no of pixels covered
    pixels = rectange_params[1][0]
    # print(pixels)
    # calculate distance
    dist = (width[mode]*focal[mode])/pixels

    return dist

for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    classNames.append(os.path.splitext(cl)[0])
# print(images[1])

# def write(x):
#     try:
#         send = bytes(str(x),"utf-8")
#         ser.write(send)
#         data = ser.readline()
#         string = data.decode()
#         if string:
#             print(string)
#         time.sleep(1)
#     except Exception as e:
#         print(e)
        # ser.close()

def findDes(images):
    desList = []
    for img in images :
        kp, des = detector.detectAndCompute(img, None)
        desList.append(des)
    return desList, kp

def findID(img, desList, thresh=20):
    global matches
    global maxlist
    kp2, des2 = detector.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = 90
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m,n in matches:
                if(m.distance<0.75*n.distance):
                    good.append([m])
            matchList.append(len(good))
        # print(matchList)
    except : 
        pass

    if len(matchList) != 0:
        if max(matchList) > thresh:
            finalVal = matchList.index(max(matchList))
    try:
        maxlist = max(matchList)
    except:
        pass
    return finalVal, kp2, matches, maxlist   

# def stackImages(scale, imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range(0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
#                     imgArray[x][y] = cv2.resize(
#                         imgArray[x][y], (0, 0), None, scale, scale)
#                 else:
#                     imgArray[x][y] = cv2.resize(
#                         imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2:
#                     imgArray[x][y] = cv2.cvtColor(
#                         imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = [imageBlank]*rows
#         hor_con = [imageBlank]*rows
#         for x in range(0, rows):
#             hor[x] = np.hstack(imgArray[x])
#         ver = np.vstack(hor)
#     else:
#         for x in range(0, rows):
#             if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
#                 imgArray[x] = cv2.resize(
#                     imgArray[x], (0, 0), None, scale, scale)
#             else:
#                 imgArray[x] = cv2.resize(
#                     imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
#             if len(imgArray[x].shape) == 2:
#                 imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor = np.hstack(imgArray)
#         ver = hor
#     return ver
theta = 9
def object_tracking(img):
    global mode
    
    global distance_obj
    global theta
    # ret, img = cap.read()

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

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # lower = np.array([hsv_lower[mode][0],hsv_lower[mode][1],hsv_lower[mode][2]])
    # upper = np.array([hsv_upper[mode][0],hsv_upper[mode][1],hsv_upper[mode][2]])
    mask = cv2.inRange(hsv_img, lower, upper)
    # thresh = cv2.threshold(mask, thresh_min, thresh_max,
    #                        cv2.THRESH_BINARY+cv2.THRESH_OTSU)
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
                
                print("dist x : ", dist_x, end="  ")
                print("dist y : ", dist_y, end="  ")
                
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
    # img_track = stackImages(0.7, ([img, d_img]))
    # cv2.imshow('ImageStack', img_track)
    return theta, distance_obj

desList, kp = findDes(images)
# print(len(desList))
cap = cv2.VideoCapture(0)

while True:
    success, img2 = cap.read()
    h,w,c = img2.shape
    imgOri = img2.copy()
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.ellipse(img2, (320,240), (80,100), 0, 0, 360, (0,0,0),-1)
    imgOri = cv2.ellipse(imgOri, (320,240), (80,100), 0, 0, 360, (0,0,0),-1)
    
    id, kp2, matches, maxlist = findID(img2, desList)
    print(str(maxlist) + " | " + str(id))
    
    if id != 90:
        # img_match = cv2.drawMatchesKnn(images[id], kp, img2, kp2, matches[:50], None, flags=2)
        cv2.putText(imgOri, "Type : " + classNames[id], (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
    # else :
    #     img_match = imgOri
    
    cv2.putText(imgOri, "N_Point : " + str(maxlist) + " | " + str(int(id)), (50,200), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    theta, distance = object_tracking(imgOri)
    data = [id,distance, theta]
    
    # if id == 5:
    #     object_tracking()
    # write(id)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(imgOri, "FPS : " + str(int(fps)),(50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    ser.write(struct.pack('>BBB', round(data[0]), round(
                    (data[1])), round((data[2]))))
    cv2.imshow("Asli", imgOri)
    # cv2.imshow("Point", img_match)
    if cv2.waitKey(1)==ord('q'):
        break