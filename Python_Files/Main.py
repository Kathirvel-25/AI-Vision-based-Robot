import cv2
import time
import HandtrackignModule as hp
import serial



cap = cv2.VideoCapture(0)
detector = hp.Hand_Tracking()
cap.set(3,1280)
cap.set(4,480)

sr = serial.Serial('COM5',9600)
time.sleep(2)


pre_command = None

while True:
     _,img = cap.read()
     img = cv2.flip(img,1)
     img,lmlist = detector.FindHand(img)
     command = None
    
     if lmlist:
          
          img,dis = detector.FindDistance(img,8,12)
          
          if lmlist[8][2] > lmlist[6][2] and\
                 lmlist[12][2] > lmlist[10][2]  and\
                 lmlist[16][2] > lmlist[14][2] and\
                 lmlist[20][2] > lmlist[18][2] and\
                 lmlist[4][1] > lmlist[3][1]:   
               
               command = 'S'

          elif lmlist[8][2] < lmlist[6][2] and\
               lmlist[12][2] < lmlist[10][2]  and\
               lmlist[16][2] < lmlist[14][2] and\
               lmlist[20][2] < lmlist[18][2] and\
               lmlist[4][1] < lmlist[3][1]:  

               command = 'F'
          elif dis < 35 and lmlist[8][2] < lmlist[6][2] and\
               lmlist[12][2] < lmlist[10][2]  and\
               lmlist[16][2] > lmlist[14][2] and\
               lmlist[20][2] > lmlist[18][2] and\
               lmlist[4][1] > lmlist[3][1]:
                
                command = 'L'
          elif dis < 35 and lmlist[8][2] < lmlist[6][2] and \
               lmlist[12][2] < lmlist[10][2] and\
               lmlist[16][2] < lmlist[14][2] and\
               lmlist[20][2] > lmlist[18][2] and\
               lmlist[4][2] > lmlist[3][2]:

                    command = 'R'

          if command != pre_command and command is not None:
               sr.write(command.encode())
               pre_command = command
               print(f"Command sent: {command}")


     img = detector.FPS(img)
     cv2.imshow("Camera",img)
     if cv2.waitKey(6) == 27:
         break
cap.release()
cv2.destroyAllWindows()

