import HTM

from cv2 import cv2
import mediapipe as mp 
import time
pt=0
ct=0
cap =cv2.VideoCapture(0)
DET=HTM.HD()
while True:
    suc,img=cap.read()
    img=DET.findHands(img)
    lmlist=DET.findpos(img)
    if len(lmlist)!=0:
        print(lmlist[4])
        ct=time.time()
        fps=1/(ct-pt)
        pt=ct
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),3)
        cv2.imshow('Image',img)
        cv2.waitKey(1)
