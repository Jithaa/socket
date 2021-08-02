from cv2 import cv2
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd='D:\\github\\Volume\\New folder\\tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe'

cap=cv2.VideoCapture(0)

def rec():
    img=cv2.imread('D:\github\Volume\images\1.png')
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    k=pytesseract.image_to_string(img)
    print(k)
    
while True:
    suc,img=cap.read()
    

    
    cv2.imshow('RES',img)

    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        os.remove('D:\github\Volume\images\1.png')
        i=1
        image = cv2.imwrite('D:\github\Volume\images\{index}.png'.format(index=i), img)
        rec()
        break
        
    



cap.release()

