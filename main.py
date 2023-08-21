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
camAngle = 0
anafi.camera_angle(currentAngle=0)

while(1):    
    while(video_stream):
        live.start()
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
            if camAngle >= -90 and camAngle <=90:
                camAngle = camAngle + 1
                anafi.camera_angle(currentAngle=camAngle)
            elif camAngle > 90:
                camAngle = 90
                print('\n\n\n\n\nMAX ANGLE REAHCED\n\n\n\n\n')
            else:
                camAngle = -90
                print('\n\n\n\n\nMAX ANGLE REAHCED\n\n\n\n\n')

        if keyboard.is_pressed('k'):
            if camAngle >= -90 and camAngle <=90:
                camAngle = camAngle - 1
                anafi.camera_angle(currentAngle=camAngle)
            elif camAngle > 90:
                camAngle = 90
                print('\n\n\n\n\nMIN ANGLE REAHCED\n\n\n\n\n')
            else:
                camAngle = -90
                print('\n\n\n\n\nMIN ANGLE REAHCED\n\n\n\n\n')

        if keyboard.is_pressed('c'):
            anafi.camera_calibrate()
            print('\n\n\n\n\n\n\n\n\n\nCAMERA CALIBRATED\n\n\n\n\n\n\n\n\n\n\n\n')