from cv2 import cv2
import mediapipe as mp 
import time
class HD():
    def __init__(self,mode=True,maxHands=2,Detect_confi=0.5,track_confi=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.Detect_confi=Detect_confi
        self.track_confi=track_confi
                
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.Detect_confi,self.track_confi)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        impRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.res=self.hands.process(impRGB)
        #print(res.multi_hand_landmarks)
        if self.res.multi_hand_landmarks:
            for handlms in self.res.multi_hand_landmarks:               
                self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)
        return(img)

    def findpos(self,img,HNo=0,draw=True):
        lmlist=[]
        if self.res.multi_hand_landmarks:
            mh=self.res.multi_hand_landmarks[HNo]
            for id,lm in enumerate(mh.landmark):
                #print(id,lm)
                h,w,c=img.shape
                c=c
                cx,cy=int(lm.x *w),int(lm.y*h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(0,0,255),cv2.FILLED)
        return lmlist

def main():
    pt=0
    ct=0
    cap =cv2.VideoCapture(0)
    DET=HD()
    while True:
        suc,img=cap.read()
        suc=suc
        img=DET.findHands(img)
        lmlist=DET.findpos(img)
        if len(lmlist)!=0:
            print(lmlist[4])
        ct=time.time()
        fps=1/(ct-pt)
        pt=ct
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)
        cv2.imshow('Image',img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()  