#File tasks . saving , opening
import tkinter as tk
from src.utils.constants import menu_bg, menu_font
from src.functions.camera import Camera

class File:
    def __init__(self, top, bottom, image_control, menubar):
        self.topFrame = top
        self.bottomFrame = bottom
        
        self.camera = None
        self.image_control = image_control
        
        #menu-bar initialization
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open image", command=self.open_image)
        self.file_menu.add_command(label="Save image", command=self.image_control.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Video camera", command=self.camera_options)
        
    def camera_options(self):
        self.image_control.hide_widget()
        self.camera = Camera(self.topFrame, self.bottomFrame, self.image_control)
        
    def open_image(self):
        if self.camera is not None:
            self.camera.hide_widget()
            del self.camera
        self.camera = None
        self.image_control.on_image()
        