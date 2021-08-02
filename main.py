from cv2 import cv2
import mediapipe as mp 
import time
cap =cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
pt=0
ct=0

while True:
    suc,img=cap.read()
    impRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=hands.process(impRGB)
    #print(res.multi_hand_landmarks)
    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x *w),int(lm.y*h)
                print(id,cx,cy)
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
    ct=time.time()
    fps=1/(ct-pt)
    pt=ct
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)

    cv2.imshow('Image',img)
    cv2.waitKey(1)
