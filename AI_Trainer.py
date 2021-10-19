import cv2
import numpy as np
import time
import PoseModule as pm

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("Curls.mp4")

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    # img = cv2.imread("test.jpg")
    # img = cv2.resize(img, (1920, 1080))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        angle = detector.findAngle(img, 11, 13, 15) #Left Arm
        # angle = detector.findAngle(img, 12, 14, 16) #Right Arm
        # angle = detector.findAngle(img, 23, 25, 27) #Left Leg
        # angle = detector.findAngle(img, 24, 26, 28) #Right Leg
        per = np.interp(angle, (70, 140), (0, 100))
        bar = np.interp(angle, (70, 140), (100, 650))
        # print(angle, per)
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count = count + 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count = count + 0.5
                dir = 0
        # print(count)
        cv2.rectangle(img, (1300, 100), (1375, 650), color, 3)
        cv2.rectangle(img, (1300, int(bar)), (1375, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(100-per)}%', (1300, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        if per==0:
            cv2.putText(img, str("Very Good !!!"), (450, 75), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)

        cv2.rectangle(img, (0, 650), (150, 820), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 745), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    # cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)