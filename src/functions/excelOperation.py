from src.utils.customErrorBox import CustomErrorBox
from src.img_control.ExcelControl import ExcelControl
from src.utils.utils import Utils
from src.utils.constants import menu_bg
from tkinter import ttk
import tkinter as tk

class ExcelOperation:
    def __init__(self, root, menubar, menu_font, image_control):
        #Excel control instance initialization
        self.excel_control = ExcelControl(image_control)
        self.message = CustomErrorBox(root)

        self.utils = Utils(root)

        #Excel menu
        self.excel_menu = tk.Menu(menubar, tearoff=0)
        self.excel_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label="Excel operatin", menu=self.excel_menu)
        self.excel_menu.add_command(label="Show matplotlib image", command=lambda: self.utils.matplotlib_show(image_control.get_image()))
        self.excel_menu.add_command(label="Threshold", command=lambda: print("threshold"))
        self.excel_menu.add_command(label="TODO", command=lambda: print("work in progress"))