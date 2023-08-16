import olympe
import cv2 as cv
import os
from .connect import connect_drone

class OlympeRstp():
    def __init__(self):

        self.drone = connect_drone()
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self.vcap = cv.VideoCapture("rtsp://192.168.42.1/live", cv.CAP_FFMPEG)

    def live_video(self):
        while(1):
            ret, frame = self.vcap.read()
            cv.imshow('VIDEO', frame)
            cv.waitKey(1)