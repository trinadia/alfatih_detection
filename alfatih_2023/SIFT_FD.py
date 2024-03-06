import cv2
import numpy as np
import os
import time
MIN_MATCH_COUNT=40

detector=cv2.SIFT_create()

pTime = 0
cTime = 0

path = "picture"
images = []
classNames = []
myList = os.listdir(path)
# detector=cv2.SIFT_create()

for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    classNames.append(os.path.splitext(cl)[0])
# print(images[1])

def findDes(images):
    desList = []
    for img in images :
        kp, des = detector.detectAndCompute(img, None)
        desList.append(des)
    return desList, kp

def findID(img, desList, thresh=32):
    kp2, des2 = detector.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m,n in matches:
                if(m.distance<0.75*n.distance):
                    good.append([m])
            matchList.append(len(good))
        print(matchList)
    except : 
        pass

    if len(matchList) != 0:
        if max(matchList) > thresh:
            finalVal = matchList.index(max(matchList))
    return finalVal, kp2, matches, matchList   

desList, kp = findDes(images)
# print(len(desList))

cap = cv2.VideoCapture(0)

while True:
    success, img2 = cap.read()
    imgOri = img2.copy()
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    id, kp2, matches, matchList = findID(img2, desList)
    if id != -1:
        img_match = cv2.drawMatchesKnn(images[id], kp, img2, kp2, matches[:50], None, flags=2)
        cv2.putText(img_match, "Type : " + classNames[id], (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
    else :
        img_match = imgOri
    
    cv2.putText(imgOri, "N_Point : " + str(int(matchList[id])) + " | " + str(int(id)), (50,200), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(imgOri, "FPS : " + str(int(fps)),(50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    # cv2.imshow("Asli", imgOri)
    cv2.imshow("Point", img_match)
    if cv2.waitKey(1)==ord('q'):
        break