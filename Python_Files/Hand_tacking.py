import cv2
import mediapipe as mp
import math
import serial
import time



model_path = "hand_landmarker.task"
# sr = serial.Serial('/dev/ttyUSB0', 9600)


cap = cv2.VideoCapture(0)

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options = mp.tasks.BaseOptions(model_asset_path = model_path),
    running_mode = mp.tasks.vision.RunningMode.VIDEO
)

landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)


tipsids = [4, 8, 12, 16, 20]
pre_command = None

while True:
    _,img = cap.read()
    img = cv2.flip(img, 1)

    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = img)
    timestamp = int(time.time() * 10000)
    result = landmarker.detect_for_video(mp_image, timestamp)

    if result.hand_landmarks:
        for handlms in result.hand_landmarks:
            finger = []
            lmlist = []
            for id, lm in enumerate(handlms):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id, cx, cy])

            x1, y1 = lmlist[8][1], lmlist[8][2]
            x2, y2 = lmlist[12][1], lmlist[12][2]

            dis = int(math.hypot(x2 - x1, y2 - y1))

            if lmlist:
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
                    lmlist[4][1] > lmlist[3][1]:

                            command = 'R'

                if command != pre_command and command is not None:
                    # sr.write(command.encode())
                    pre_command = command
                    print(command)


    img = cv2.imshow("Computer_vision", img)
    key = cv2.waitKey(4)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()