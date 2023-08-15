import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import tkinter as tk
from tkinter import filedialog

def convert_to_temperature(pixel_value, min_temp_k, max_temp_k):
    return ((pixel_value / 255) * (max_temp_k - min_temp_k) + min_temp_k) - 273.15

def save_image(temperature_image):
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)    
    image_number = 1
    while os.path.exists(os.path.join(output_folder, f"thermal{image_number}.tif")):
        image_number += 1    
    output_path = os.path.join(output_folder, f"thermal{image_number}.tif")
    cv2.imwrite(output_path, temperature_image.astype(np.float32))    
    print(f"Image saved as: {output_path}")


def main():
    root = tk.Tk()
    root.withdraw()
    
    image_path = filedialog.askopenfilename(title="Select a grayscale image", filetypes=[("Image files", "*.jpg *.png *.bmp *.JPG")])
    if not image_path:
        print("No image selected. Exiting.")
        return
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)    
    min_temp_k = float(input("Enter the minimum temperature (in Kelvin): "))
    max_temp_k = float(input("Enter the maximum temperature (in Kelvin): "))    
    inferno_cmap = LinearSegmentedColormap.from_list('inferno', plt.cm.inferno(np.linspace(0, 1, 256))    
    temperature_image_c = convert_to_temperature(image, min_temp_k, max_temp_k)
    save_image(temperature_image_c)    
    plt.figure(figsize=(10, 6))
    plt.imshow(temperature_image_c, cmap=inferno_cmap)
    plt.colorbar(label='Temperature (°C)')
    plt.title("Thermal Image with Temperature Mapping")
    plt.xlabel("X")
    plt.ylabel("Y")
    
    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            x = int(event.xdata)
            y = int(event.ydata)
            temperature_at_point = temperature_image_c[y, x]
            print(f"Temperature at point ({x}, {y}): {temperature_at_point:.2f} °C")
    
    plt.connect('button_press_event', onclick)
    plt.show()


if __name__ == "__main__":
    main()
