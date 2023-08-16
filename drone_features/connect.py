import olympe

DRONE_IP = "192.168.42.1"  # Change this to the appropriate IP
DRONE_MEDIA_PORT = "80"     # Change this if needed

def connect_drone():
    drone = olympe.Drone(DRONE_IP, media_port=DRONE_MEDIA_PORT)
    drone.connect(timeout=10, retry=3)
    return drone
