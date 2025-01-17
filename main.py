import tkinter as tk
from src.app import App
        
if __name__ == "__main__":
    root = tk.Toplevel()
    
    icon = tk.PhotoImage(file = 'src/public/research.png')
    root.iconphoto(False, icon)
    #print(tk.font.families())
     
    #Menubar initialization
    menubar = tk.Menu(root) 
    app = App(root, menubar)
    root.config(menu=menubar)
    root.mainloop()  
