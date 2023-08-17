import time
import keyboard
from drone_features.connection import connect, disconnect
from drone_features.rstp_streaming import Rstp
from drone_features.thermal import Thermal
from drone_features.thermal_display import compute_temperature
from drone_features.control import Command

drone = connect()
thermal = Thermal(drone)
video_stream = True
live = Rstp()
anafi = Command(drone)

while(1):    
    while(video_stream):
        live.live_video()
        if keyboard.is_pressed('q'):
            video_stream = False
            disconnect()
            exit()

        if keyboard.is_pressed('p'):
            thermal.take_real_photo()   
            time.sleep(1)
            print("\n\n\n\n\n\n\n\nReady for Input\n\n\n\n\n\n\n\n")
            compute_temperature(thermal.photo)
            live = Rstp()

        if keyboard.is_pressed('w'):
            anafi.forward()

        if keyboard.is_pressed('s'):
            anafi.backward()

        if keyboard.is_pressed('d'):
            anafi.right()

        if keyboard.is_pressed('a'):
            anafi.left()

        if keyboard.is_pressed('t'):
            anafi.takeoff()

        if keyboard.is_pressed('l'):
            anafi.land()

        if keyboard.is_pressed('space'):
            anafi.stop()

        if keyboard.is_pressed('left'):
            anafi.rotate_left()

        if keyboard.is_pressed('right'):
            anafi.rotate_right()

        if keyboard.is_pressed('h'):
            anafi.home()

        if keyboard.is_pressed('i'):
            anafi.camera_up()

        if keyboard.is_pressed('k'):
            anafi.camera_down()

        if keyboard.is_pressed('c'):
            anafi.camera_calibrate()
            print('\n\n\n\n\n\n\n\n\n\nCAMERA CALIBRATED\n\n\n\n\n\n\n\n\n\n\n\n')