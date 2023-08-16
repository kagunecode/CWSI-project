import olympe
import tempfile
import re
import xml.etree.ElementTree as ET
from connect import connect_drone
from logging import getLogger
from olympe.media import (
    indexing_state,
    download_media
)
from olympe.messages.camera2.Event import Photo
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
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

class OlympeThermal():

    def __init__(self):
        self.drone = connect_drone()

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

    def take_real_photo(self):
        assert self.drone.media(
            indexing_state(state="indexed")
        ).wait(_timeout=60).success()
        self.setup_photo_mode()
        self.real_drone()

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
        logger = getLogger("photo_example")
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
        resources = media_download.as_completed(expected_count=photo_count, timeout=60)
        resource_count = 0
        for resource in resources:
            logger.info(f"Resource: {resource.resource_id}")
            if not resource.success():
                logger.error(f"Failed to download {resource.resource_id}")
                continue
            resource_count += 1
            with open(resource.download_path, "rb") as image_file:
                image_data = image_file.read()
                image_xmp_start = image_data.find(b"<x:xmpmeta")
                image_xmp_end = image_data.find(b"</x:xmpmeta")
                if image_xmp_start < 0 or image_xmp_end < 0:
                    logger.error(f"Failed to find XMP photo metadata {resource.resource_id}")
                    continue
                image_xmp = ET.fromstring(image_data[image_xmp_start: image_xmp_end + 12])
                for image_meta in image_xmp[0][0]:
                    xmp_tag = re.sub(r"{[^}]*}", "", image_meta.tag)
                    xmp_value = image_meta.text
                    if xmp_tag in self.XMP_TAGS_OF_INTEREST:
                        logger.info(f"{resource.resource_id} {xmp_tag} {xmp_value}")
        logger.info(f"{resource_count} media resource downloaded")
        assert resource_count == 14, f"resource count == {resource_count} != 14"

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


if __name__ == '__main__':
    drone = OlympeThermal()
    drone.take_real_photo()