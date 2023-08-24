import tkinter as tk
from drone_features.rstp_streaming import Rstp
from drone_features.camera import Camera
from drone_features.thermal_display import plot_temperature
from drone_features.control import Command
from drone_features.connection import disconnect
from  drone_features.status import Status
import multiprocessing as mp
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import mplcursors
import numpy as np
import cv2

class GUI:
    def __init__(self, drone):
        self.root = tk.Tk()
        self.root.title("Anafi Control")
        self.drone = drone
        self.anafi = Command(self.drone)
        self.camAngle = 0
        self.camera = Camera(self.drone)
        self.live = Rstp()
        self.state = Status(self.drone)

        self.movement_frame = tk.Frame(self.root)
        self.movement_frame.grid(row=2, column=0, columnspan=5)
        self.elevation_frame = tk.Frame(self.root)
        self.elevation_frame.grid(row=2, column=5, columnspan=5)
        self.command_bar = tk.Frame(self.root)
        self.command_bar.grid(row=4, column=0, columnspan=10)
        self.empty_row = tk.Frame(self.root, height=10)
        self.empty_row.grid(row=3, column=0)
        self.status_bar = tk.Frame(self.root)
        self.status_bar.grid(row=5, column=0, columnspan=10)

        self.landing_button = tk.Button(self.command_bar, text="Land", command=self.landing)
        self.takeoff_button = tk.Button(self.command_bar, text="Take Off", command=self.takeoff)
        self.forward_button = tk.Button(self.movement_frame, text="Forward", command=self.forward)
        self.backward_button = tk.Button(self.movement_frame, text="Backward", command=self.backward)
        self.left_button = tk.Button(self.movement_frame, text="Left", command=self.left)
        self.right_button = tk.Button(self.movement_frame, text="Right", command=self.right)
        self.camera_up_button = tk.Button(self.command_bar, text="Cam Up", command=self.camera_up)
        self.camera_down_button = tk.Button(self.command_bar, text="Cam Down", command=self.camera_down)
        self.photo_button = tk.Button(self.command_bar, text="Photo", command=self.take_photo)
        self.thermal_photo_button = tk.Button(self.command_bar, text="Thermal Photo", command=self.take_thermal_photo)
        self.drone_up_button = tk.Button(self.elevation_frame, text="Elevate", command=self.drone_up)
        self.drone_down_button = tk.Button(self.elevation_frame, text="Lower", command=self.drone_down)
        self.rotate_left_button = tk.Button(self.elevation_frame, text="Rotate Left", command=self.rotate_left)
        self.rotate_right_button = tk.Button(self.elevation_frame, text="Rotate Right", command=self.rotate_right)
        self.quit_button = tk.Button(self.command_bar, text="Quit", command=self.quit)
        self.home_button = tk.Button(self.command_bar, text="Return Home", command=self.home, bg="red", fg="white")
        self.show_hide_button = tk.Button(self.root, text="Show/Hide Canvas", command=self.toggle_canvas)
        self.battery_label = tk.Label(self.status_bar, text=self.state.battery())
        
        self.show_hide_button.grid(row=1, column=0, columnspan=10)
        self.forward_button.grid(row=1, column=1)
        self.backward_button.grid(row=3, column=1)
        self.left_button.grid(row=2, column=0)
        self.right_button.grid(row=2, column=2)
        self.camera_up_button.grid(row=0, column=0)
        self.camera_down_button.grid(row=0, column=1)
        self.photo_button.grid(row=0, column=2)
        self.thermal_photo_button.grid(row=0, column=3)
        self.takeoff_button.grid(row=0, column=4)
        self.landing_button.grid(row=0, column=6)
        self.drone_up_button.grid(row=1, column=6)
        self.drone_down_button.grid(row=3, column=6)
        self.rotate_left_button.grid(row=2, column=5)
        self.rotate_right_button.grid(row=2, column=7)
        self.quit_button.grid(row=0, column=8)
        self.home_button.grid(row=0, column=7)
        self.battery_label.grid(row=0, column=0)

        self.canvas_visible = True
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=10)

        self.root.bind("<KeyPress-w>", lambda event: self.handle_key_press(event, self.forward_button, self.forward))
        self.root.bind("<KeyRelease-w>", lambda event: self.handle_key_release(event, self.forward_button))

        self.root.bind("<KeyPress-s>", lambda event: self.handle_key_press(event, self.backward_button, self.backward))
        self.root.bind("<KeyRelease-s>", lambda event: self.handle_key_release(event, self.backward_button))

        self.root.bind("<KeyPress-a>", lambda event: self.handle_key_press(event, self.left_button, self.left))
        self.root.bind("<KeyRelease-a>", lambda event: self.handle_key_release(event, self.left_button))

        self.root.bind("<KeyPress-d>", lambda event: self.handle_key_press(event, self.right_button, self.right))
        self.root.bind("<KeyRelease-d>", lambda event: self.handle_key_release(event, self.right_button))

        self.root.bind("<KeyPress-t>", lambda event: self.handle_key_press(event, self.takeoff_button, self.takeoff))
        self.root.bind("<KeyRelease-t>", lambda event: self.handle_key_release(event, self.takeoff_button))

        self.root.bind("<KeyPress-i>", lambda event: self.handle_key_press(event, self.camera_up_button, self.camera_up))
        self.root.bind("<KeyRelease-i>", lambda event: self.handle_key_release(event, self.camera_up_button))

        self.root.bind("<KeyPress-k>", lambda event: self.handle_key_press(event, self.camera_down_button, self.camera_down))
        self.root.bind("<KeyRelease-k>", lambda event: self.handle_key_release(event, self.camera_down_button))

        self.root.bind("<KeyPress-n>", lambda event: self.handle_key_press(event, self.photo_button, self.take_photo))
        self.root.bind("<KeyRelease-n>", lambda event: self.handle_key_release(event, self.photo_button))

        self.root.bind("<KeyPress-p>", lambda event: self.handle_key_press(event, self.thermal_photo_button, self.take_thermal_photo))
        self.root.bind("<KeyRelease-p>", lambda event: self.handle_key_release(event, self.thermal_photo_button))

        self.root.bind("<KeyPress-l>", lambda event: self.handle_key_press(event, self.landing_button, self.landing))
        self.root.bind("<KeyRelease-l>", lambda event: self.handle_key_release(event, self.landing_button))

        self.root.bind("<KeyPress-Up>", lambda event: self.handle_key_press(event, self.drone_up_button, self.drone_up))
        self.root.bind("<KeyRelease-Up>", lambda event: self.handle_key_release(event, self.drone_up_button))

        self.root.bind("<KeyPress-Down>", lambda event: self.handle_key_press(event, self.drone_down_button, self.drone_down))
        self.root.bind("<KeyRelease-Down>", lambda event: self.handle_key_release(event, self.drone_down_button))

        self.root.bind("<KeyPress-Left>", lambda event: self.handle_key_press(event, self.rotate_left_button, self.rotate_left))
        self.root.bind("<KeyRelease-Left>", lambda event: self.handle_key_release(event, self.rotate_left_button))

        self.root.bind("<KeyPress-Right>", lambda event: self.handle_key_press(event, self.rotate_right_button, self.rotate_right))
        self.root.bind("<KeyRelease-Right>", lambda event: self.handle_key_release(event, self.rotate_right_button))
                
        self.root.bind("<KeyPress-q>", lambda event: self.handle_key_press(event, self.quit_button, self.quit))
        self.root.bind("<KeyRelease-q>", lambda event: self.handle_key_release(event, self.quit_button))

        self.root.bind("<KeyPress-h>", lambda event: self.handle_key_press(event, self.home_button, self.home))
        self.root.bind("<KeyRelease-h>", lambda event: self.handle_key_release(event, self.home_button)) 

        self.root.bind("<KeyPress-space>", lambda event: self.handle_key_press(event, self.show_hide_button, self.toggle_canvas))
        self.root.bind("<KeyRelease-space>", lambda event: self.handle_key_release(event, self.show_hide_button)) 
        

        for button in [self.forward_button, self.backward_button, self.left_button, self.right_button,
                       self.camera_up_button, self.camera_down_button, self.photo_button, self.thermal_photo_button,
                       self.drone_up_button, self.drone_down_button, self.rotate_left_button, self.rotate_right_button,
                       self.quit_button, self.home_button, self.takeoff_button, self.landing_button]:
            button.configure(width=10, height=2)            
 
    def forward(self):
        self.anafi.forward()
        print(self.state.battery())

    def backward(self):
        self.anafi.backward()

    def left(self):
        self.anafi.left()

    def right(self):
        self.anafi.right()

    def takeoff(self):
        self.anafi.takeoff()

    def landing(self):
        self.anafi.land()

    def drone_up(self):
        self.anafi.up()

    def drone_down(self):
        self.anafi.down()

    def rotate_left(self):
        self.anafi.rotate_left()

    def rotate_right(self):
        self.anafi.rotate_right()

    def toggle_canvas(self):
        if self.canvas_visible:
            self.canvas.get_tk_widget().grid_forget()
            self.canvas_visible = False
        else:
            self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=10)
            self.canvas_visible = True

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

    def camera_down(self):
        if self.camAngle >= -90 and self.camAngle <=90:
            self.camAngle = self.camAngle - 1
            self.anafi.camera_angle(currentAngle=self.camAngle)
        elif self.camAngle > 90:
            self.camAngle = 90
            print('\n\n\n\n\nMIN ANGLE REAHCED\n\n\n\n\n')
        else:
            self.camAngle = -90
            print('\n\n\n\n\nMIN ANGLE REAHCED\n\n\n\n\n')

    def take_photo(self):
        self.camera.take_real_photo(photo_type='normal')   
        time.sleep(1)
        print("\n\n\n\n\n\n\n\nReady for Input\n\n\n\n\n\n\n\n")
        self.live = Rstp()

    def take_thermal_photo(self):
        self.camera.take_real_photo(photo_type='thermal')
        print("\n\n\n\n\n\n\n\nReady for Input\n\n\n\n\n\n\n\n")
        time.sleep(1)
        plot_temperature(self.camera.photo, self.figure, self.ax, self.canvas)
        self.live = Rstp()        

    def handle_key_press(self, event, button, command):
        button.config(relief=tk.SUNKEN)
        command()

    def handle_key_release(self, event, button):
        button.config(relief=tk.RAISED)

    def live_video(self):
        self.live.start()

    def live_video_loop(self):
        self.live_video()
        self.root.after(1, self.live_video_loop)

    def battery_level(self):
        self.root.after(1, self.battery_level)
        print(self.state.cam_angle())
        self.battery_label.config(text="Battery: "+str(self.state.battery())+"%")

    def home(self):
        self.anafi.home()

    def quit(self):
        disconnect()
        exit()

    def run(self):
        self.live_video_loop()
        self.battery_level()
        self.root.mainloop()