# motion-detector
---
Motion Detector with Websocket, OpenCV, Golang, Python

Dependencies:

Golang:

1. gorilla/websocket

Python:

1. websocket-client
2. opencv

Protobuf


How to run:

1. Under the server folder, run the server with `go run server.go`

2. Then go to the client folder, run the client `python client.py`

3. I used opencv built-in method to connect the webcamera, and if motion is detected, it will save the image file in result folder, with timestamp in the file name.
