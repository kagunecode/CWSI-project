import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, CancelMoveBy, NavigateHome
from olympe.messages.camera2.Command import Configure, StartPhoto
from olympe.messages.camera2.Event import Photo
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    take_photo,
    photo_progress,
    camera_capabilities,
    set_white_balance
)
from olympe.media import download_media, indexing_state
from olympe.enums.camera import model
from olympe.messages.thermal import set_mode, set_rendering, set_palette_settings, set_sensitivity, set_palette_part, set_emissivity, set_background_temperature
from logging import getLogger
import keyboard
import requests
import shutil
import tempfile
import xml.etree.ElementTree as ET
import re

olympe.log.update_config({
    "loggers": {
        "olympe": {"level": "INFO"},
        "photo_example": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }
})

logger = getLogger("photo_example")

# NOTE: IP Can differ if connected with drone WIFI, SkyControl or Sim.
# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1") # For simulated drone.
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1") # 42 wifi, 53 control.
DRONE_MEDIA_PORT = os.environ.get("DRONE_MEDIA_PORT", "80")
XMP_TAGS_OF_INTEREST = (
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


def drone_connect():
    print("\n" * 5)
    print("CONNECTING TO THE DRONE, PLEASE WAIT")
    print("\n" * 5)
    drone = olympe.Drone(DRONE_IP, media_port=DRONE_MEDIA_PORT) # Media port needed to connect to the drone server.
    drone.connect(timeout=5, retry=3)
    key_test(drone)


def key_test(drone):
    print("\n" * 5)
    print("KEYBOARD CONTROLS STARTED")
    print("USE THE ARROWS TO MOVE")
    print("PRESS 'T' TO TAKEOFF")
    print("PRESS 'L' TO LAND")
    print("PRESS R FOR REAL DRONE PHOTO")
    print("PRESS J FOR AVAILABLE CAMERAS")
    print("\n" * 5)

    while True:
        keyboard.on_press_key('t', lambda _:
        drone(TakeOff()))
        keyboard.on_press_key('l', lambda _:
        drone(Landing()))
        keyboard.on_press_key('up', lambda _:
        drone(moveBy(1, 0, 0, 0)))
        keyboard.on_press_key('j', lambda _:
        drone(model))
        keyboard.on_press_key('down', lambda _:
        drone(moveBy(-1, 0, 0, 0)))
        keyboard.on_press_key('right', lambda _:
        drone(moveBy(0, 1, 0, 0)))
        keyboard.on_press_key('left', lambda _:
        drone(moveBy(0, -1, 0, 0)))
        keyboard.on_press_key('space', lambda _:
        drone(CancelMoveBy()))
        keyboard.on_press_key('r', lambda _:
        take_real_photo(drone))
        keyboard.on_press_key('esc', lambda _:
        drone.disconnect())
        break
    keyboard.wait()


def take_real_photo(drone):
    assert drone.media(
        indexing_state(state="indexed")
    ).wait(_timeout=60).success()
    setup_photo_burst_mode(drone)
    test_real_drone(drone)
    drone.disconnect()


def test_real_drone(drone):
    photo_saved = drone(photo_progress(result="photo_saved", _policy="wait"))
    drone(take_photo(cam_id=1)).wait()
    if not photo_saved.wait(_timeout=30).success():
        assert False, "take_photo timedout"
    photo_progress_info = photo_saved.received_events().last().args
    media_id = photo_progress_info["media_id"]
    photo_count = photo_progress_info["photo_count"]
    drone.media.download_dir = tempfile.mkdtemp(prefix="olympe_photo_example")
    logger.info(
        "Download photo burst resources for media_id: {} in {}".format(
            media_id,
            drone.media.download_dir,
        )
    )
    media_download = drone(download_media(media_id, integrity_check=True))
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
                if xmp_tag in XMP_TAGS_OF_INTEREST:
                    logger.info(f"{resource.resource_id} {xmp_tag} {xmp_value}")
    logger.info(f"{resource_count} media resource downloaded")
    assert resource_count == 14, f"resource count == {resource_count} != 14"

def setup_photo_burst_mode(drone):
    drone(set_mode(mode="standard")) # command message olympe.messages.thermal.set_mode(mode, _timeout=10, _no_expect=False, _float_tol=(1e-07, 1e-09))
    # Thermal modes standard, disabled, blended. Should disable camera? cam_id 1 apparently is for video only.
    # No Thermal support for streaming video.
    drone(set_rendering(mode="thermal", blending_rate=0))
    drone(set_palette_settings(mode="absolute", lowest_temp=300, highest_temp=314, outside_colorization="limited", 
                               relative_range="locked", spot_type="hot", spot_threshold=290))
    drone(set_sensitivity(range="low")) 
    drone(set_emissivity(emissivity=1))
    drone(set_camera_mode(cam_id=1, value="photo")).wait()
    drone(
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
    drone_connect()