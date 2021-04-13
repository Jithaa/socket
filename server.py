import socket,pickle,struct,time
from cv2 import cv2
SS=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
hostname=socket.gethostname()
ip=socket.gethostbyname(hostname)
print(hostname,ip)
PORT=2501
SA=(ip,PORT)
SS.bind(SA)
SS.listen(5)
pt=0
while True:
    cl_socket,addr=SS.accept()
    print("CONNECTED TO",addr)
    if cl_socket:
        cap=cv2.VideoCapture(0)
        suc,img=cap.read()
        ct=time.time()
        fps=1/(ct-pt)
        pt=ct
        cv2.putText(img,str(int(fps)),(10,20),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),3)
        a=pickle.dumps(img)
        msg=struct.pack("Q",len(a))+a
        cl_socket.sendall(msg)
        cv2.imshow("VIDEO",img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            cl_socket.close()

