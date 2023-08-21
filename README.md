# CWSI-project
Project related to the CWSI calculation

# UPDATES
Using Olympe 7.5.0 since Oylmpe 7.7.0 causes constant connection retries. This has been fixed on the current version of this program. Requirements have been updated to use the functional Olympe version.
Multiprocessing is being used as of now in this program since matplotlib blocks the program from executing any following code. For now, it's the best solution as it has no impact on the performance of the live stream video at all.
Also, the venv used needs a cleanup since there are a lot of packages that are not being used at all.

**0.1.0**: Added camera capabilities to take photo. Basic functions are still on progress.<br />
**0.2.0**: Added thermal camera capabilities for photo mode only.<br />
**0.3.0**: Updated the project structure to work in a modular way.<br />
**0.3.1**: The thermal module runs on a new process in order to prevent blocking due to matplotlib.<br />
**0.4.0**: Added live video stream from the drone directly. Added basic commands.<br />
**0.4.1**: Improved video delay changing the bitrate of the video. Now when taking a thermal photo the final result is shown immediatly.<br />
**0.5.0**: Added camera angle control. Yaw and Roll are disabled by default since most drones don't support it anyways. Camera angle gets reset to 0 every time you run the program again, this
has to be changed for future versions of the program.

# CONTROLS
As of the latest stable version (**0.5.0**) the controls are:<br /><br />
**W - A - S - D**: Control the drone directions (up, left, down and right).<br />
**ARROWS**: Left and right will rotate the drone to that direction. Up and down will make the drone go higher or lower.<br />
**H**: The drone will try to come back to the landing point (home). This might not work if the drone loses connection or if it has no battery left.<br />
**T**: Takeoff. The Drone will make a sound to warn about the takeoff. You can cancel it by sending a landing request<br />.
**L**: Landing. Please make sure there's enough space for the drone to land. Also, lower the drone as much as you can before sending a land request.<br />
**P**: Take thermal photo. The process takes a couple seconds and you get the image saved in the images/drone directory. If you don't have this directory the program will likely crash.<br />
**I - K**: Control the camera angle. I goes up and K goes down.<br />
**C**: Calibrate camera. If you notice any errors on the camera angle run this request and it should get fixed.<br />
**Q**: Quits the program. Take in count this wont make the drone come back nor land. Quit the program when you're done.<br />