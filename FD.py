from cv2 import cv2
import mediapipe as mp 
import time
cap =cv2.VideoCapture(0)
mpFace=mp.solutions.face_mesh
face=mpFace.FaceMesh()
mpDraw=mp.solutions.drawing_utils
pt=0
while True:
    success,img=cap.read()
    ImgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=face.process(img)
    if results.multi_face_landmarks:
        for flms in results.multi_face_landmarks:
            for id,lm in enumerate(flms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x *w),int(lm.y*h)
                print(id,cx,cy)
                cv2.circle(img,(cx,cy),2,(0,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img,flms,mpFace.FACE_CONNECTIONS)
    ct=time.time()
    fps=1/(ct-pt)
    pt=ct
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),3)

    cv2.imshow('Image',img)
    cv2.waitKey(1)