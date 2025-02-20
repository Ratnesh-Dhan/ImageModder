# zoom zoomout, redo undo
import tkinter as tk
from src.utils.constants import menu_bg
from src.utils.customErrorBox import CustomErrorBox
import cv2

class Edit:
    def __init__(self, root, image_control, menubar, menu_font):
        self.root = root
        self.image_control = image_control
        self.message = CustomErrorBox(root)
        
        self.edit_menu = tk.Menu(menubar, tearoff=0)
        self.edit_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=image_control.undo)
        self.edit_menu.add_command(label="Redo", command=image_control.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Zoom in", command=image_control.zoom_in)
        self.edit_menu.add_command(label="Zoom out", command=image_control.zoom_out)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="grayscale", command=self.grayscale)
        self.edit_menu.add_command(label="BGR to HSV", command=self.bgr2hsv)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Red Channel", command=self.red_channel)
        self.edit_menu.add_command(label="Green Channel", command=self.green_channel)
        self.edit_menu.add_command(label="Blue Channel", command=self.blue_channel)
        
    def red_channel(self):
        try:        
            img = self.image_control.get_image()
            if img.ndim == 3:  # Check if the image has color channels (3D array)
                red_channel = img[:, :, 0]  # Extract the red channel (first channel)
                self.image_control.load_image(red_channel)
            else:
                raise ValueError("The image does not have color channels.")
        except ValueError as e:
            self.message.show("Caution", e)
        except Exception as e:
            self.message.show("Error", e)

    def green_channel(self):
        try:        
            img = self.image_control.get_image()
            if img.ndim == 3:  # Check if the image has color channels (3D array)
                red_channel = img[:, :, 1]  # Extract the red channel (first channel)
                self.image_control.load_image(red_channel)
            else:
                raise ValueError("The image does not have color channels.")
        except ValueError as e:
            self.message.show("Caution", e)
        except Exception as e:
            self.message.show("Error", e)

    def blue_channel(self):
        try:        
            img = self.image_control.get_image()
            if img.ndim == 3:  # Check if the image has color channels (3D array)
                red_channel = img[:, :, 2]  # Extract the red channel (first channel)
                self.image_control.load_image(red_channel)
            else:
                raise ValueError("The image does not have color channels.")
        except ValueError as e:
            self.message.show("Caution", e)
        except Exception as e:
            self.message.show("Error", e)
    
    def grayscale(self):
        try:
            img = self.image_control.get_image()
            if img is not None:
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                self.image_control.load_image(gray_image)
            else:
                raise ValueError("😟 The image is not loaded. Please load an image before processing.")
        except Exception as e:
            print(e)
            self.message.show("Error", e)
        
    def bgr2hsv(self):
        try:
            img = self.image_control.get_image()
            if img is not None:
                hsvimage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                self.image_control.load_image(hsvimage)
            else:
                raise ValueError("😟 The image is not loaded. Please load an image before processing.")
        except Exception as e:
            print(e)
            self.message.show("Error", e)
            