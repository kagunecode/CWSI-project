from olympe.messages.ardrone3.Piloting import TakeOff, Landing, CancelMoveBy, PCMD, NavigateHome
from olympe.messages.ardrone3.Sound import StartAlertSound, StopAlertSound
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.camera import set_alignment_offsets, reset_alignment_offsets
from olympe.messages.gimbal import set_offsets, start_offsets_update, stop_offsets_update, calibrate, set_target
import time

class Command:
    def __init__(self, drone):
        self.drone = drone


    def takeoff(self):
        self.drone(StartAlertSound())
        time.sleep(2)
        self.drone(StopAlertSound())
        self.drone(TakeOff())

    def land(self):
        self.drone(Landing())

    def right(self):
        self.drone(PCMD(flag=1, roll=30, pitch=0, yaw=0, gaz=0, timestampAndSeqNum=1))

    def left(self):
        self.drone(PCMD(flag=1, roll=-30, pitch=0, yaw=0, gaz=0, timestampAndSeqNum=1))

    def forward(self):
        self.drone(PCMD(flag=1, roll=0, pitch=30, yaw=0, gaz=0, timestampAndSeqNum=1))
        
    def backward(self):
        self.drone(PCMD(flag=1, roll=0, pitch=-30, yaw=0, gaz=0, timestampAndSeqNum=1))

    def rotate_left(self):
        self.drone(PCMD(flag=1, roll=0, pitch=0, yaw=-100, gaz=0, timestampAndSeqNum=1))

    def rotate_right(self):
        self.drone(PCMD(flag=1, roll=0, pitch=0, yaw=100, gaz=0, timestampAndSeqNum=1))

    def up(self):
        self.drone(PCMD(flag=1, roll=0, pitch=0, yaw=0, gaz=10, timestampAndSeqNum=1))        

    def down(self):
        self.drone(PCMD(flag=1, roll=0, pitch=0, yaw=0, gaz=-10, timestampAndSeqNum=1))  

    def stop(self):
        self.drone(CancelMoveBy())

    def home(self):
        self.drone(NavigateHome(start=-1))

    def camera_angle(self, currentAngle):
        self.drone(set_target(
        gimbal_id=0,
        control_mode="position",
        yaw_frame_of_reference="none", # Yaw is not supported in the Anafi Thermal, you could change this if your drone supports it.
        yaw=0,
        pitch_frame_of_reference="absolute",
        pitch=currentAngle,
        roll_frame_of_reference="none", # Same with roll, some drones might support it so change it if you need to.
        roll=0,
        ))
        return currentAngle

    def camera_calibrate(self):
        self.drone(calibrate(gimbal_id=0))