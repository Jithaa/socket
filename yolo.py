from cv2 import cv2
import time
import numpy as np 
import HTM
import FDM
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
wc,hc=720,720
cap=cv2.VideoCapture(1)
cap.set(3,wc)
cap.set(4,hc)
pt=0
DET=HTM.HD(Detect_confi=0.9)
DE=FDM.FD(min_detection_confidence=0.9)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vr=volume.GetVolumeRange()

minVol=vr[0]
maxVol=vr[1]
while True:
    suc,img=cap.read()
    img=DET.findHands(img)
    lmlist=DET.findpos(img,draw=False)
    img=DE.findFace(img)
    flmlist=DE.lm(img,draw=False)
    if  flmlist==0:
        print("No Face Detected")
    if len(lmlist)!=0:
        
        #4-thumb 8- index
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),5,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),5,(0,255,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
        l=math.hypot(x2-x1,y2-y1)
        vol=np.interp(l,[30,150],[minVol,maxVol])
        volb=np.interp(l,[30,150],[400,150])
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        
        
        if l<50:
            cv2.circle(img,(cx,cy),5,(0,255,255),cv2.FILLED)
            cv2.rectangle(img,(50,int(volb)),(85,400),(0,255,0),cv2.FILLED)
        elif l>130:
            cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
            cv2.rectangle(img,(50,int(volb)),(85,400),(0,0,255),cv2.FILLED)
        else:
            cv2.rectangle(img,(50,int(volb)),(85,400),(0,255,0),cv2.FILLED)

        



    ct=time.time()
    fps=1/(ct-pt)
    pt=ct
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)
    cv2.imshow("img",img)
    cv2.waitKey(1)

