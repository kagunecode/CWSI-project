from drone_features.thermal import OlympeThermal
from drone_features.streaming import OlympeStreaming
from drone_features.rstp_streaming import OlympeRstp

drone = OlympeThermal()
drone.take_real_photo()
print("PHOTO TAKEN")

drone = OlympeRstp()
drone.live_video()