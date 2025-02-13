from src.utils.customErrorBox import CustomErrorBox
from src.img_control.ExcelControl import ExcelControl
from src.utils.utils import Utils
from src.utils.constants import menu_bg
from tkinter import ttk
import tkinter as tk

class ExcelOperation:
    def __init__(self, root, menubar, menu_font, custom_font, image_control):
        self.root = root
        self.custom_font = custom_font
        #Excel control instance initialization
        self.excel_control = ExcelControl(image_control)
        self.message = CustomErrorBox(root)
        
        self.utils = Utils(root)

        #Excel menu
        self.excel_menu = tk.Menu(menubar, tearoff=0)
        self.excel_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label="Excel operatin", menu=self.excel_menu)
        self.excel_menu.add_command(label="Show matplotlib image", command=lambda: self.utils.matplotlib_show(image_control.get_image()))
        self.excel_menu.add_command(label="Threshold", command=self.threshold)
        
    def threshold(self):
        try:
            def apply_threshold():
                value = int(entry1.get())
                bool = self.excel_control.value_thershold(value)
                if(bool):
                    self.message.show("Sucess", "Applied")
            new_window = tk.Toplevel(self.root)
            new_window.title("Threshold")
            #Setting height and width of the window
            window_width = 220
            window_height = 150
            #Setting the window on center
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            #Adding widget on the floating window
            ttk.Label(new_window, text="Set pixel Threshold", font=self.custom_font).pack(pady=10)
            entry1 = ttk.Entry(new_window, width=10, font=('Helvetica', 12))  # Increase the width and set the font size
            entry1.insert(0, "0.0")
            entry1.pack(pady=10, ipady=5)  # Increase the height by adding internal padding
            ttk.Button(new_window, text="Apply", command=apply_threshold).pack( pady=10, ipadx=5, ipady=3)

        except ValueError as e:
            self.message.show("Error", "Value should be floating/integer number.")
        except Exception as e:
            self.message.show("Error", e)
