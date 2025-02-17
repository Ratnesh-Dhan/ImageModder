import tkinter as tk
from src.app import App
import sys
import os
from src.utils.constants import initialize_fonts
        
if __name__ == "__main__":
    # root = tk.Toplevel()
    if getattr(sys, 'frozen', False):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(BASE_DIR, "src", "public", "research.png")
    image_path = os.path.normpath(image_path)

    root = tk.Tk()
    icon = tk.PhotoImage(file = image_path)
    root.iconphoto(False, icon)
    #print(tk.font.families())
    
    #initialize fonts
    custom_font, label_font, button_font, menu_font = initialize_fonts()
     
    #Menubar initialization
    menubar = tk.Menu(root) 
    app = App(root, menubar, custom_font, label_font, button_font, menu_font)
    root.config(menu=menubar)
    root.mainloop()  


    # THIS IS PYINSTALLER COMMAND

    # pyinstaller --onefile --windowed --add-data "src/public/*;src/public" --icon=src/public/mainIcon.ico main.py
