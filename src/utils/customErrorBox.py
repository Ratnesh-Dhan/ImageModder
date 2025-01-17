import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CustomErrorBox:
    def __init__(self, root):
        
        self.root = root
        self.font = tk.font.Font(size=13,weight=tk.font.BOLD, family='Comic Sans MS')
        
    def show(self, title, message):
        if title == 'Caution':
            img = 'src/public/caution.png'
        elif title == 'Error':
            img = 'src/public/cancel.png'
        elif title == 'Sucess':
            img = 'src/public/checked.png'
        else:
            img = 'src/public/cancel.png'
            
        
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
        