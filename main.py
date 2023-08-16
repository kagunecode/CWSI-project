from drone_features.rstp_streaming import OlympeRstp
from drone_features.thermal import OlympeThermal
from drone_features.connect import connect_drone

thermal = OlympeThermal()
thermal.take_real_photo()

live = OlympeRstp()
live.live_video()