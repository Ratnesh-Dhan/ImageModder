import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CustomErrorBox:
    def __init__(self, root):
        
        self.root = root
        self.font = tk.font.Font(size=13,weight=tk.font.BOLD, family='Comic Sans MS')
        
    def show(self, title, message):

        if getattr(sys, 'frozen', False):
            BASE_DIR = sys._MEIPASS
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        caution_path = os.path.join(BASE_DIR, "src", "public", "caution.png")
        caution_path = os.path.normpath(caution_path)
        cancel_path = os.path.join(BASE_DIR, "src", "public", "cancel.png")
        cancel_path = os.path.normpath(cancel_path)
        checked_path = os.path.join(BASE_DIR, "src", "public", "checked.png")
        checked_path = os.path.normpath(checked_path)
        # cancel_path = os.path.join(BASE_DIR, "public/cancel.png")

        if title == 'Caution':
            # img = 'src/public/caution.png'
            img = caution_path
        elif title == 'Error':
            # img = 'src/public/cancel.png'
            img = cancel_path
        elif title == 'Success':
            # img = 'src/public/checked.png'
            img = checked_path
        else:
            # img = 'src/public/cancel.png'
            img = cancel_path
            
        
        photo = Image.open(img)
        photo = photo.resize((50,50))
        photo = ImageTk.PhotoImage(photo)
        top = tk.Toplevel(self.root)
        top.title(title)
        top.iconphoto(False, photo)
        
        frame = tk.Frame(top)
        frame.pack(padx=(20,0), pady=(10,5), fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(frame)
        inner_frame.pack()
        
        icon_label = tk.Label(inner_frame, image=photo)
        icon_label.image = photo  
        icon_label.pack(side=tk.LEFT, padx=10)
        
        label = ttk.Label(inner_frame, text=message, wraplength=400, font=self.font)
        
        # # Set maximum width for the Text widget
        # max_width = 400  # Set your desired maximum width here
        # label = tk.Text(inner_frame, wrap=tk.WORD, font=self.font, bg=top.cget('bg'), bd=0)
        
        # # Insert the message and configure the Text widget
        # label.insert(tk.END, message)
        # label.config(state=tk.DISABLED)  # Make it read-only
        
        # # Calculate the required width and height
        # label.update_idletasks()  # Update the widget to get the current size
        # required_width = min(label.winfo_reqwidth(), max_width)
        # label.config(width=required_width // 5)  # Width in text units (approx. 10 pixels per unit)
        # # Calculate the number of lines in the message
        # num_lines = message.count('\n') + 1  # Count lines based on newlines
        # label.config(height=num_lines)  # Set height based on number of lines
    
        label.pack(padx=10, pady=(20,10),ipadx=10, fill=tk.BOTH, expand=True)
        button = ttk.Button(frame, text="OK", command=top.destroy)
        button.pack(pady=10, side=tk.BOTTOM)
        
        # Update the window's layout
                #update_idletasks method to update the window's layout before setting its geometry
        top.update_idletasks()

        # Get the window's width and height
        # width = label.winfo_reqwidth() + 40
        # height = label.winfo_reqheight() + button.winfo_reqheight() + 40
        
        width = frame.winfo_reqwidth()+40
        height = frame.winfo_reqheight()+20
        
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        top.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        