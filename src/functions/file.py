#File tasks . saving , opening
import tkinter as tk
from src.utils.constants import menu_bg
from src.functions.camera import Camera
from src.utils.utils import Utils

class File:
    def __init__(self, root, top, bottom, image_control, pixel_works, menubar, menu_font): 
        self.topFrame = top
        self.bottomFrame = bottom
        self.root = root
        
        self.camera = None
        self.image_control = image_control
        self.pixel_works = pixel_works
        self.utils = Utils(root)

        #menu-bar initialization
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open image", command=self.open_image)
        # self.file_menu.add_command(label="this is test", command=lambda: print("hello world"))
        self.file_menu.add_command(label="Open excel file as image", command=self.open_excel)
        self.file_menu.add_command(label="Save image", command=self.image_control.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Video camera", command=self.camera_options)
        
    def camera_options(self):
        self.image_control.hide_widget()
        self.camera = Camera(self.topFrame, self.bottomFrame, self.image_control)
        self.pixel_works.reset_all()
        
    def open_image(self):
        if self.camera is not None:
            self.camera.hide_widget()
            del self.camera
        self.camera = None
        self.image_control.on_image()
        self.utils.fit_to_screen(self.image_control, self.bottomFrame)
        self.pixel_works.reset_all()

    def open_excel(self):
        if self.camera is not None:
            self.camera.hide_widget()
            del self.camera
        self.camera = None
        self.image_control.open_excel()
        self.pixel_works.reset_all()

        