from src.utils.customErrorBox import CustomErrorBox
from src.img_control.ExcelControl import ExcelControl
from src.utils.utils import Utils
from src.utils.constants import menu_bg
from tkinter import ttk
import tkinter as tk

class ExcelOperation:
    def __init__(self, root, menubar, menu_font, custom_font, label_font, image_control):
        self.root = root
        self.custom_font = custom_font
        self.label_font = label_font

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
        self.excel_menu.add_command(label="Square each pixels", command=self.excel_control.pixel_square)
        self.excel_menu.add_command(label="Add value to pixel", command=self.add_val)
        
    def threshold(self):
        try:
            def apply_threshold():
                try:
                    lower = float(entry1.get())  
                    upper = float(entry2.get())
                    bool = self.excel_control.value_thershold(lower, upper)
                    if(bool):
                        new_window.destroy()
                        self.message.show("Success", "Applied 😊")
                except ValueError:
                    self.message.show("Caution", "Values should be integer or floating")
            new_window = tk.Toplevel(self.root)
            new_window.title("Threshold")
            #Setting height and width of the window
            window_width = 220
            window_height = 230
            #Setting the window on center
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            #Adding widget on the floating window
            ttk.Label(new_window, text="Set pixel Threshold", font=self.custom_font).pack(pady=10)
            frame1 = tk.Frame(new_window)
            frame1.pack()
            ttk.Label(frame1, text="Lower :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            entry1 = ttk.Entry(frame1, width=10, font=('Helvetica', 12))  # Increase the width and set the font size
            entry1.insert(0, "0.0")
            entry1.pack(side=tk.RIGHT,padx=(10,0) , pady=10, ipady=5)  # Increase the height by adding internal padding
            ttk.Label(new_window, text="------optional-------", font=('Arial', 10, 'italic')).pack()
            frame2 = tk.Frame(new_window)
            frame2.pack(pady=(5,10))
            ttk.Label(frame2, text="Upper :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            entry2 = ttk.Entry(frame2, width=10, font=('Helvetica', 12))
            entry2.insert(0, "0.0")
            entry2.pack(side=tk.RIGHT,padx=(10,0), ipady=5)
            ttk.Button(new_window, text="Apply", command=apply_threshold).pack( pady=(10,0), ipadx=5, ipady=3)

        except ValueError as e:
            self.message.show("Error", "Value should be floating/integer number.")
        except Exception as e:
            self.message.show("Error", e)

    def add_val(self):
        def addValue():
            try:
                try:
                    pixel_value = float(entry1.get())
                except ValueError:
                    raise ValueError("Entry 1 must be a float.")
                
                try:
                    value = int(entry2.get())
                except ValueError:
                    raise ValueError("Entry 2 must be an integer.")
                bool = self.excel_control.add_value_to_pixels(value, pixel_value)
                if bool:
                    self.message.show("Success", "Adjustment successful! 🎉")
                else:
                    self.message.show("Error","😟 Oops! Something went wrong. Please check your inputs and try again.")
            except ValueError as e:
                self.message.show("Error", e)
            
        new_window = tk.Toplevel(self.root)
        new_window.title("Adjust Pixel Intensity")
        #Setting height and width of the window
        window_width = 220
        window_height = 180
        #Setting the window on center
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width//2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        ttk.Label(new_window, text="Adjust Pixel Intensity", font=self.custom_font).pack(pady=10)
        frame1 = tk.Frame(new_window)
        frame1.pack(pady=(0, 10))
        ttk.Label(frame1, text="Threshold Value:", font=self.label_font).pack(side=tk.LEFT, padx=(0, 5))
        entry1 = ttk.Entry(frame1, width=6, font=('Helvetica', 12))
        entry1.insert(0, "0.0")
        entry1.pack(side=tk.RIGHT)
        frame2 = tk.Frame(new_window)
        frame2.pack(pady=(0, 10))
        ttk.Label(frame2, text="Increment Value:", font=self.label_font).pack(side=tk.LEFT, padx=(0,5))
        entry2 = ttk.Entry(frame2, width=6, font=('Helvetica', 12))
        entry2.insert(0, "0")
        entry2.pack(side=tk.RIGHT)
        ttk.Button(new_window, text="Apply Adjustment", command=addValue).pack(pady=(10,0), ipadx=5, ipady=3)