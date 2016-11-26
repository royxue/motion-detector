import time
import cv2
import imutils
import msg_pb2
from websocket import create_connection

cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()

frame1 = imutils.resize(frame1, width=400)
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
prvs = cv2.GaussianBlur(prvs, (21, 21), 0)
avg = (cv2.GaussianBlur(prvs, (21, 21), 0)).copy().astype("float")

ws = create_connection("ws://127.0.0.1:8080/")

while True:
    ret, frame2 = cap.read()

    frame2 = imutils.resize(frame2, width=400)

    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    next = cv2.GaussianBlur(next, (21, 21), 0)
    cv2.accumulateWeighted(next, avg, 0.5)

    frameDelta = cv2.absdiff(next, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    for c in cnts:
        if cv2.contourArea(c) > (frame2.shape[0]*frame2.shape[1]) * 0.05:
            msg = msg_pb2.msg()
            msg.cid = "montion_detected"
            msg.timestamp = str(time.time())
            msg.height = frame2.shape[0]
            msg.width = frame2.shape[1]
            msg.image = (cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)).tostring()
            ws.send(msg.SerializeToString())
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

    cv2.imshow('Motion Detector', frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    prvs = next

ws.close()
cap.release()
cv2.destroyAllWindows()
