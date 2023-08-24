import tkinter as tk
from drone_features.rstp_streaming import Rstp
from drone_features.camera import Camera
from drone_features.thermal_display import compute_temperature
from drone_features.control import Command
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

        self.landing_button = tk.Button(self.root, text="Land", command=self.landing)
        self.takeoff_button = tk.Button(self.root, text="Take Off", command=self.takeoff)
        self.forward_button = tk.Button(self.root, text="W", command=self.forward)
        self.backward_button = tk.Button(self.root, text="S", command=self.backward)
        self.left_button = tk.Button(self.root, text="A", command=self.left)
        self.right_button = tk.Button(self.root, text="D", command=self.right)
        self.camera_up_button = tk.Button(self.root, text="Cam Up", command=self.camera_up)
        self.camera_down_button = tk.Button(self.root, text="Cam Down", command=self.camera_down)
        self.photo_button = tk.Button(self.root, text="Photo", command=self.take_photo)
        self.thermal_photo_button = tk.Button(self.root, text="Thermal Photo", command=self.take_thermal_photo)

        self.show_hide_button = tk.Button(self.root, text="Show/Hide Canvas", command=self.toggle_canvas)
        self.show_hide_button.grid(row=8, column=0, columnspan=10)

        self.forward_button.grid(row=0, column=1)
        self.backward_button.grid(row=2, column=1)
        self.left_button.grid(row=1, column=0)
        self.right_button.grid(row=1, column=2)
        self.camera_up_button.grid(row=6, column=1)
        self.camera_down_button.grid(row=7, column=1)
        self.photo_button.grid(row=4, column=1)
        self.thermal_photo_button.grid(row=4, column=0)
        self.takeoff_button.grid(row=1, column=5, columnspan=2)
        self.landing_button.grid(row=2, column=5, columnspan=2)

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
 
    def forward(self):
        self.anafi.forward()

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

    def toggle_canvas(self):
        if self.canvas_visible:
            self.canvas.get_tk_widget().grid_forget()
            self.canvas_visible = False
        else:
            self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=10)
            self.canvas_visible = True


    def plot_temperature(self, photo):
        image_path = "images/drone/" + photo

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        min_temp_k = 274
        max_temp_k = 314
        inferno_cmap = LinearSegmentedColormap.from_list('inferno', plt.cm.inferno(np.linspace(0, 1, 256)))
        temperature_image_c = self.convert_to_temperature(image, min_temp_k, max_temp_k)

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        im = self.ax.imshow(temperature_image_c, cmap=inferno_cmap, aspect='auto')
        plt.colorbar(im, ax=self.ax, label='Temperature (°C)')
        plt.title("Thermal Image with Temperature Mapping")
        mplcursors.cursor(hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f"Temperature: {temperature_image_c[sel.target.index]:.2f} °C"))
        self.canvas.draw()

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
        self.plot_temperature(self.camera.photo)
        self.live = Rstp()

    def convert_to_temperature(self, pixel_value, min_temp_k, max_temp_k):
        return ((pixel_value / 255) * (max_temp_k - min_temp_k) + min_temp_k) - 273.15
        

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