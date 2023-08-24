import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib
matplotlib.use("Agg")
import mplcursors
import os
import multiprocessing as mp

def convert_to_temperature(pixel_value, min_temp_k, max_temp_k):
        return ((pixel_value / 255) * (max_temp_k - min_temp_k) + min_temp_k) - 273.15

def plot_temperature(photo, figure, ax, canvas):
    image_path = "images/drone/" + photo

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    min_temp_k = 274
    max_temp_k = 314
    inferno_cmap = LinearSegmentedColormap.from_list('inferno', plt.cm.inferno(np.linspace(0, 1, 256)))
    temperature_image_c = convert_to_temperature(image, min_temp_k, max_temp_k)

    figure.clear()
    ax = figure.add_subplot(111)
    im = ax.imshow(temperature_image_c, cmap=inferno_cmap, aspect='auto')
    plt.colorbar(im, ax=ax, label='Temperature (°C)')
    plt.title("Thermal Image with Temperature Mapping")
    mplcursors.cursor(hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(f"Temperature: {temperature_image_c[sel.target.index]:.2f} °C"))
    canvas.draw()