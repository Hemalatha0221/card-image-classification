import cv2
import numpy as np
import time
import winsound 
from datetime import datetime

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = cv2.QRCodeDetector()
log_file = "qr_log.txt"
last_value = ""

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    start = time.perf_counter()
    value, points, _ = detector.detectAndDecode(img)

    if points is not None and value != "":
        points = points[0]
        x1, y1 = points[0]
        x2, y2 = points[2]

        x_center = int((x2 - x1) / 2 + x1)
        y_center = int((y2 - y1) / 2 + y1)

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (159, 43, 104), 3)
        cv2.circle(img, (x_center, y_center), 5, (207, 159, 255), -1)
        cv2.putText(img, f"Data: {value}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (119, 7, 55), 2)

        if value != last_value:
            last_value = value
            print(f"[+] New QR Detected: {value}")
            winsound.Beep(1000, 300)
            with open(log_file, "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - {value}\n")

    end = time.perf_counter()
    fps = 1 / (end - start)
    cv2.putText(img, f"FPS: {fps:.2f}", (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow('QR Code Scanner', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
