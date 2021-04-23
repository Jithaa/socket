import socket,pickle,struct,time

from cv2 import cv2


cl_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host_ip='26.126.177.24'
port=25010
k=(host_ip,port)
cl_socket.connect(k)

data=b''
payload_size=struct.calcsize("Q")

while True:
    while len(data)<payload_size:
        packet=cl_socket.recv(512)
        if not packet:break
        data+=packet

    packed_msg=data[:payload_size]
    dat=data[payload_size:]   
    msg_size=struct.unpack("Q",packed_msg)[0]


    while len(dat)<msg_size:

        data+=cl_socket.recv(512)

    frame=data[:msg_size]

    data=data[msg_size:]
    print("work")
    frame=pickle.loads(frame)

    cv2.imshow("out",frame)
    
cl_socket.close()
