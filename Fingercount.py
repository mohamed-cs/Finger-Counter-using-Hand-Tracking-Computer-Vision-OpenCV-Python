import pyautogui as pyautogui

import os
import time

import imutils
import numpy as np
import cv2 as cv
import math
import HandTrackingModule as ht


def returcameraind():
    index=-2
    arr=[]
    i=10

    while i>0:
        cap=cv.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index+=1
        i-=1

    return arr

camacess=returcameraind()[0]

wcam, hcam = 800, 480
ptime=0

cv.namedWindow("preview")
cap = cv.VideoCapture(camacess)

if not (cap.isOpened()):
   print("Could not open video device")

folderpath="fingers"
fingerplist=os.listdir(folderpath)

imgfullpathlist=[]
for imagepath in fingerplist:
    image=cv.imread(fr"{folderpath}/{imagepath}")
    imgfullpathlist.append(image)


detector=ht.handDetector()

while True:

    success, img = cap.read()


    img=imutils.resize(img, width=wcam,height=hcam)
    img=detector.findHands(img)
    fingerlist=list(detector.findPosition(img,draw=False))
    count=0
    listtop=[8,12,16,20]
    listbottom=[6,10,14,18]

    if len(fingerlist[0])!=0:

        for i in range(4):
            if fingerlist[0][listtop[i]][2] < fingerlist[0][listbottom[i]][2]:
                count+=1
        if  fingerlist[0][12][1] < fingerlist[0][8][1]:
            if fingerlist[0][4][1] > fingerlist[0][3][1]:
                count += 1
        else:
            if fingerlist[0][4][1] < fingerlist[0][3][1]:
                count += 1
        print(count)

        h, w, c = imgfullpathlist[count].shape
        img[0:h, 0:w] = imgfullpathlist[count]



    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv.putText(img, f"Fps :{int(fps)}", (200, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 1)

    cv.imshow("Image", img)
    cv.waitKey(1)