import tkinter as tk
from src.app import App
from src.utils.constants import initialize_fonts
        
if __name__ == "__main__":
    # root = tk.Toplevel()
    root = tk.Tk()
    print("test")
    icon = tk.PhotoImage(file = 'src/public/research.png')
    root.iconphoto(False, icon)
    #print(tk.font.families())
    
    #initialize fonts
    custom_font, label_font, button_font, menu_font = initialize_fonts()
     
    #Menubar initialization
    menubar = tk.Menu(root) 
    app = App(root, menubar, custom_font, label_font, button_font, menu_font)
    root.config(menu=menubar)
    root.mainloop()  
