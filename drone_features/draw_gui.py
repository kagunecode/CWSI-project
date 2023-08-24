import tkinter as tk
from drone_features.rstp_streaming import Rstp
from drone_features.camera import Camera
from drone_features.thermal_display import compute_temperature
from drone_features.control import Command
import time

class GUI:
    def __init__(self, drone):
        self.root = tk.Tk()
        self.root.title("Anafi Control")
        self.drone = drone
        self.anafi = Command(self.drone)
        self.camAngle = 0
        self.camera = Camera(self.drone)
        self.live = Rstp()


        self.forward_button = tk.Button(self.root, text="W", command=self.forward)
        self.backward_button = tk.Button(self.root, text="S", command=self.backward)
        self.left_button = tk.Button(self.root, text="A", command=self.left)
        self.right_button = tk.Button(self.root, text="D", command=self.right)
        self.camera_up_button = tk.Button(self.root, text="Cam Up", command=self.camera_up)
        self.photo_button = tk.Button(self.root, text="Photo", command=self.take_photo)

        self.forward_button.grid(row=0, column=1)
        self.backward_button.grid(row=2, column=1)
        self.left_button.grid(row=1, column=0)
        self.right_button.grid(row=1, column=2)
        self.camera_up_button.grid(row=6, column=1)
        self.photo_button.grid(row=4, column=1)

        self.root.bind("<KeyPress-w>", lambda event: self.handle_key_press(event, self.forward_button, self.forward))
        self.root.bind("<KeyRelease-w>", lambda event: self.handle_key_release(event, self.forward_button))

        self.root.bind("<KeyPress-s>", lambda event: self.handle_key_press(event, self.backward_button, self.backward))
        self.root.bind("<KeyRelease-s>", lambda event: self.handle_key_release(event, self.backward_button))

        self.root.bind("<KeyPress-a>", lambda event: self.handle_key_press(event, self.left_button, self.left))
        self.root.bind("<KeyRelease-a>", lambda event: self.handle_key_release(event, self.left_button))

        self.root.bind("<KeyPress-d>", lambda event: self.handle_key_press(event, self.right_button, self.right))
        self.root.bind("<KeyRelease-d>", lambda event: self.handle_key_release(event, self.right_button))


        self.root.bind("<KeyPress-i>", lambda event: self.handle_key_press(event, self.camera_up_button, self.camera_up))
        self.root.bind("<KeyRelease-i>", lambda event: self.handle_key_release(event, self.camera_up_button))




        self.root.bind("<KeyPress-n>", lambda event: self.handle_key_press(event, self.photo_button, self.take_photo))
        self.root.bind("<KeyRelease-n>", lambda event: self.handle_key_release(event, self.photo_button))



    def forward(self):
        print("Forward function")

    def backward(self):
        print("Backward function")

    def left(self):
        print("Left function")

    def right(self):
        print("Right function")

    def camera_up(self):
        if self.camAngle >= -90 and self.camAngle <=90:
            self.camAngle = self.camAngle + 1
            self.anafi.camera_angle(currentAngle=self.camAngle)
        elif self.camAngle > 90:
            self.camAngle = 90
            print('\n\n\n\n\nMAX ANGLE REAHCED\n\n\n\n\n')
        else:
            self.camAngle = -90
            print('\n\n\n\n\nMAX ANGLE REAHCED\n\n\n\n\n')

    def take_photo(self):
        self.camera.take_real_photo(photo_type='normal')   
        time.sleep(1)
        print("\n\n\n\n\n\n\n\nReady for Input\n\n\n\n\n\n\n\n")
        self.live = Rstp()



    def handle_key_press(self, event, button, action_function):
        button.config(relief=tk.SUNKEN)
        action_function()

    def handle_key_release(self, event, button):
        button.config(relief=tk.RAISED)

    def live_video(self):
        self.live.start()

    def live_video_loop(self):
        self.live_video()
        self.root.after(1, self.live_video_loop)


    def run(self):
        self.live_video_loop()
        self.root.mainloop()