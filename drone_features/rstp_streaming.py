import cv2 as cv
import os
import time

class Rstp():
    def __init__(self):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self.vcap = cv.VideoCapture("rtsp://192.168.42.1/live", cv.CAP_FFMPEG)
        self.vcap.set(cv.CAP_PROP_BUFFERSIZE, 1)
        self.loop = True

    def start(self):
        ret, frame = self.vcap.read()
        cv.imshow('VIDEO', frame)
        cv.waitKey(1)

