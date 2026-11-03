
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import subprocess

# Mac-compatible system volume control
def set_mac_volume(percent):
    percent = int(np.clip(percent, 0, 100))
    subprocess.run(
        [
            "osascript",
            "-e",
            f"set volume output volume {percent}"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

pTime = 0
lastVolume = -1
lastUpdate = 0

detector = htm.handDetector(detectionCon=0.77)

volPer = 0
volBar = 350

try:
    while True:
        success, img = cap.read()

        if not success:
            print("Could not access webcam.")
            break

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10,
                       (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10,
                       (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2),
                     (255, 0, 255), 2)
            cv2.circle(img, (cx, cy), 8,
                       (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            # Map finger distance to Mac volume percentage
            volPer = int(np.clip(
                np.interp(length, [25, 250], [0, 100]),
                0, 100
            ))
            volBar = np.interp(length, [25, 250], [350, 150])

            # Avoid calling AppleScript on every frame
            now = time.time()
            if (lastVolume == -1
                    or abs(volPer - lastVolume) >= 2
                    or now - lastUpdate >= 0.25):
                set_mac_volume(volPer)
                lastVolume = volPer
                lastUpdate = now

            if length < 30:
                cv2.circle(img, (cx, cy), 8,
                           (0, 255, 0), cv2.FILLED)

            cv2.putText(
                img, f"Volume: {volPer}%",
                (100, 100), cv2.FONT_HERSHEY_COMPLEX,
                0.7, (0, 255, 0), 2
            )

        cv2.rectangle(img, (50, 150), (75, 350),
                      (0, 255, 0), 2)
        cv2.rectangle(
            img, (50, int(volBar)), (75, 350),
            (0, 255, 0), cv2.FILLED
        )
        cv2.putText(
            img, f"{int(volPer)} %",
            (44, 390), cv2.FONT_HERSHEY_COMPLEX,
            0.6, (200, 0, 0), 2
        )

        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime else 0
        pTime = cTime

        cv2.putText(
            img, f"FPS: {int(fps)}",
            (35, 50), cv2.FONT_HERSHEY_COMPLEX,
            0.7, (255, 0, 0), 2
        )

        cv2.imshow("Mac Gesture Volume Controller", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
