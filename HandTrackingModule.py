
import cv2
import mediapipe as mp


class handDetector:
    def __init__(
        self,
        mode=False,
        maxHands=2,
        detectionCon=0.5,
        trackCon=0.5
    ):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(
            static_image_mode=mode,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.draw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if draw and self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.draw.draw_landmarks(
                    img,
                    hand,
                    self.hands_module.HAND_CONNECTIONS
                )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []

        if (
            self.results.multi_hand_landmarks
            and len(self.results.multi_hand_landmarks) > handNo
        ):
            hand = self.results.multi_hand_landmarks[handNo]
            height, width, _ = img.shape

            for index, landmark in enumerate(hand.landmark):
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                lmList.append([index, x, y])

                if draw:
                    cv2.circle(img, (x, y), 5, (255, 0, 255), cv2.FILLED)

        return lmList
