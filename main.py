import time
import keyboard
from drone_features.connection import connect, disconnect
from drone_features.rstp_streaming import Rstp
from drone_features.thermal import Thermal
from drone_features.trhemal_display import compute_temperature

drone = connect()
thermal = Thermal(drone)
video_stream = True
live = Rstp()
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
