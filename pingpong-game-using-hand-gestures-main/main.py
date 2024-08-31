import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgBackground = cv2.imread("res/Background.png")
imgGameOver = cv2.imread("res/game over.png")
imgBall = cv2.imread("res/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("res/paddle1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("res/paddle2.png", cv2.IMREAD_UNCHANGED)

detector = HandDetector(detectionCon=0.8, maxHands=2)
playerA = input('enter name of playerA:')
playerB = input('enter name of playerB:')
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    hands, img = detector.findHands(img, flipType=False)

    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    if hands:

        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        if score[0]>score[1]:
            cv2.putText(img, str(score[0]).zfill(2), (670, 640), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 255, 255), 3)
            cv2.putText(img, str(playerA +' won'), (500, 590), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        else:
            cv2.putText(img, str(score[1]).zfill(2), (670, 640), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            cv2.putText(img, str(playerB + ' won'), (500, 590), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.putText(img,playerA, (550, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),3)
        cv2.putText(img,playerB, (850, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),3)
        cv2.putText(img, str(score[0]).zfill(2), (550, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.putText(img, str(score[1]).zfill(2), (850, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    else:
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        img = cvzone.overlayPNG(img, imgBall, ballPos)
        cv2.putText(img, str(playerA), (300, 550), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)
        cv2.putText(img, str(playerB), (900, 550), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

        cv2.putText(img, str(score[0]).zfill(2), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        cv2.putText(img, str(score[1]).zfill(2), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("r"):
            ballPos = [100, 100]
            speedX = 15
            speedY = 15
            gameOver = False
            score = [0, 0]
            imgGameOver = cv2.imread("res/game over.png")


