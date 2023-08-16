import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, CancelMoveBy, NavigateHome
from olympe.messages.camera2.Command import Configure, StartPhoto
from olympe.messages.camera2.Event import Photo
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    take_photo,
    photo_progress,
    camera_capabilities,
    set_white_balance
)
from olympe.media import download_media, indexing_state
from olympe.enums.camera import model
from olympe.messages.thermal import set_mode, set_rendering, set_palette_settings, set_sensitivity, set_emissivity
from logging import getLogger
import keyboard
import requests
import shutil
import tempfile
import xml.etree.ElementTree as ET
import re

def key_test(drone):
    print("\n" * 5)
    print("KEYBOARD CONTROLS STARTED")
    print("USE THE ARROWS TO MOVE")
    print("PRESS 'T' TO TAKEOFF")
    print("PRESS 'L' TO LAND")
    print("PRESS R FOR REAL DRONE PHOTO")
    print("PRESS J FOR AVAILABLE CAMERAS")
    print("\n" * 5)

    while True:
        keyboard.on_press_key('t', lambda _:
        drone(TakeOff()))
        keyboard.on_press_key('l', lambda _:
        drone(Landing()))
        keyboard.on_press_key('up', lambda _:
        drone(moveBy(1, 0, 0, 0)))
        keyboard.on_press_key('j', lambda _:
        drone(model))
        keyboard.on_press_key('down', lambda _:
        drone(moveBy(-1, 0, 0, 0)))
        keyboard.on_press_key('right', lambda _:
        drone(moveBy(0, 1, 0, 0)))
        keyboard.on_press_key('left', lambda _:
        drone(moveBy(0, -1, 0, 0)))
        keyboard.on_press_key('space', lambda _:
        drone(CancelMoveBy()))
        keyboard.on_press_key('r', lambda _:
        take_real_photo(drone))
        keyboard.on_press_key('esc', lambda _:
        drone.disconnect())
        break
    keyboard.wait()

if __name__ == '__main__':
    drone_connect()