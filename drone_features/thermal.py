import olympe
import tempfile
import re
import time
import xml.etree.ElementTree as ET
from logging import getLogger
from olympe.media import (
    indexing_state,
    download_media
)
from olympe.messages.camera2.Event import Photo
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    set_streaming_mode,
    take_photo,
    photo_progress
)
from olympe.messages.thermal import (
    set_mode, 
    set_rendering, 
    set_palette_settings, 
    set_sensitivity, 
    set_emissivity
)
import shutil
import requests

class Thermal():

    def __init__(self, drone):
        self.drone = drone

        self.XMP_TAGS_OF_INTEREST = (
            "CameraRollDegree",
            "CameraPitchDegree",
            "CameraYawDegree",
            "CaptureTsUs",
            # NOTE: GPS metadata is only present if the drone has a GPS fix
            # (i.e. they won't be present indoor).
            "GPSLatitude",
            "GPSLongitude",
            "GPSAltitude",            
        )

        self.photo = 0

    def take_real_photo(self):
        assert self.drone.media(
            indexing_state(state="indexed")
        ).wait(_timeout=60).success()
        self.setup_photo_mode()
        self.real_drone()
        self.drone(set_mode(mode="disabled"))
        #self.drone.disconnect()

    def real_drone(self):
        olympe.log.update_config({
            "loggers": {
                "olympe": {"level": "INFO"},
                "photo_example": {
                    "level": "INFO",
                    "handlers": ["console"],
                }
            }
        })
        logger = getLogger("olympe")
        photo_saved = self.drone(photo_progress(result="photo_saved", _policy="wait"))
        self.drone(take_photo(cam_id=1)).wait()
        if not photo_saved.wait(_timeout=30).success():
            assert False, "take_photo timeout"
        photo_progress_info = photo_saved.received_events().last().args
        media_id = photo_progress_info["media_id"]
        photo_count = photo_progress_info["photo_count"]
        self.drone.media.download_dir = tempfile.mkdtemp(prefix="olympe_photo_example")
        logger.info(
            "Download photo burst resources for media_id: {} in {}".format(
                media_id,
                self.drone.media.download_dir,
            )            
        )
        media_download = self.drone(download_media(media_id, integrity_check=True))
        time.sleep(2)
        media_string = str(media_download).split('resource_id=')
        photo_id = media_string[1].split(")")
        url = 'http://192.168.42.1:80/data/media/'+photo_id[0]
        response = requests.get(url)
        self.photo = photo_id[0]
        with open('images/drone/'+photo_id[0], "wb") as f:
            f.write(response.content)


        #assert resource_count == 14, f"resource count == {resource_count} != 14"

    def setup_photo_mode(self):
        self.drone(set_mode(mode="standard")) # command message olympe.messages.thermal.set_mode(mode, _timeout=10, _no_expect=False, _float_tol=(1e-07, 1e-09))
        # Thermal modes standard, disabled, blended. Should disable camera? cam_id 1 apparently is for video only.
        # No Thermal support for streaming video.
        self.drone(set_rendering(mode="thermal", blending_rate=0))
        self.drone(set_palette_settings(mode="absolute", lowest_temp=274, highest_temp=314, outside_colorization="limited", 
                               relative_range="locked", spot_type="hot", spot_threshold=290))
        self.drone(set_sensitivity(range="low")) 
        self.drone(set_emissivity(emissivity=1))
        self.drone(set_camera_mode(cam_id=1, value="photo")).wait()
        self.drone(
            set_photo_mode(
                cam_id=1,
                mode="single",
                format="rectilinear",
                file_format="dng_jpeg",
                burst="burst_14_over_1s",
                bracketing="preset_1ev",
                capture_interval=0.0,
            )
        ).wait().success()


#if __name__ == '__main__':
#    drone = OlympeThermal()
#    drone.take_real_photo()