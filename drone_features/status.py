import olympe
from olympe.messages.common.CommonState import BatteryStateChanged

class Status:
    def __init__(self, drone):
        self.drone = drone
    
    def battery(self):
        return self.drone.get_state(BatteryStateChanged)['percent']