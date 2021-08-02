from cv2 import cv2
import mediapipe as mp 
import time
class FD():
    def __init__(self,mode=False,max_num_faces=1,min_detection_confidence=0.95):
        self.mode=mode
        self.max_num_faces=max_num_faces
        self.min_detection_confidence=min_detection_confidence

        self.mpFace=mp.solutions.face_mesh
        self.face=self.mpFace.FaceMesh(self.mode,self.max_num_faces,self.min_detection_confidence)
        self.mpDraw=mp.solutions.drawing_utils
    
    def findFace(self,img):
        self.ImgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.face.process(img)
        if self.results.multi_face_landmarks:
            for flms in self.results.multi_face_landmarks:
               
                self.mpDraw.draw_landmarks(img,flms,self.mpFace.FACE_CONNECTIONS)
        return(img)
    def lm(self,img,fno=0,draw=False):
        flmlist=[]
        if self.results.multi_face_landmarks:
            mf=self.results.multi_face_landmarks[fno]
            for id,lm in enumerate(mf.landmark):
                #print(id,lm)
                h,w,c=img.shape
                c=c
                cx,cy=int(lm.x *w),int(lm.y*h)
                flmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),1,(0,0,255),-1)
        else:
            flmlist=0
        return flmlist

def main():
    pt=0
    ct=0
    cap =cv2.VideoCapture(0)
    DET=FD()
    while True:
        suc,img=cap.read()
        suc=suc
        img=DET.findFace(img)
        flmlist=DET.lm(img)
        if len(flmlist)!=0:
            print(flmlist[4])
        ct=time.time()
        fps=1/(ct-pt)
        pt=ct
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)
        cv2.imshow('Image',img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()  
