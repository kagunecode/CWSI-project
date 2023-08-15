import cv2
import tkinter as tk
from tkinter import filedialog

def get_temp(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        temp = img[y, x]
        print('Temperatura en la Coordenada ({}, {}): {}'.format(x, y, temp))

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
img = cv2.imread(file_path, -1)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

img = cv2.resize(img, (int(screen_width*0.8), int(screen_height*0.8)))

cv2.imshow('Imagen Termica', img)
cv2.setMouseCallback('Imagen Termica', get_temp)
cv2.waitKey(0)
cv2.destroyAllWindows()
