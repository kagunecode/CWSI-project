import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

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


def main(photo):    
    image_path = "images/drone/"+photo
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)    
    min_temp_k = 274
    max_temp_k = 314   
    inferno_cmap = LinearSegmentedColormap.from_list('inferno', plt.cm.inferno(np.linspace(0, 1, 256)))
    temperature_image_c = convert_to_temperature(image, min_temp_k, max_temp_k) 
    plt.figure(figsize=(10, 6))
    plt.plot()
    plt.imshow(temperature_image_c, cmap=inferno_cmap)
    plt.colorbar(label='Temperature (°C)')
    plt.title("Thermal Image with Temperature Mapping")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()