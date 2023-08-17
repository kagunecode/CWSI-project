import olympe

DRONE_IP = "192.168.42.1"  # 42 for Wifi drone, 53 for SkyController
DRONE_MEDIA_PORT = "80"     # Port 80 works fine as it's open
drone = olympe.Drone(DRONE_IP, media_port=DRONE_MEDIA_PORT)

def connect():
    drone.connect()
    return drone

def disconnect():
    drone.disconnect()
    