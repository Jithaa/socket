import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import FDM
import HTM
import math
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.6', 2501))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 2048);
cam.set(4, 2048);

img_counter = 0
pt=0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
DET=HTM.HD(Detect_confi=0.7)
DE=FDM.FD(min_detection_confidence=0.7)
while True:
    ret, img = cam.read()
    img=DET.findHands(img)
    lmlist=DET.findpos(img,draw=True)
    img=DE.findFace(img)
    flmlist=DE.lm(img,draw=True)
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
        cv2.circle(img,(cx,cy),5,(0,255,255),cv2.FILLED) 
    ct=time.time()
    fps=1/(ct-pt)
    pt=ct
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)
    result, frame = cv2.imencode('.jpg', img, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()