import sys
import tkinter as tk
from tkinter import ttk
#from src.utils.image_utils import ImageViewer
from src.img_control.ImageControl import ImageControl
from src.functions.filters import CustomFilters
from src.functions.graphs import Graphs
from src.functions.file import File
from src.functions.edit import Edit
# from PIL import Image, ImageTk

class App:
    def __init__(self, root, menubar, custom_font, label_font, button_font, menu_font):
        self.root = root
        self.root.title("ImageModder")
        self.root.geometry("800x500")
        self.root.config(bg="#79D7BE")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
        self.style = ttk.Style(root)
        # self.style.configure('TButton', background="#F6F4F0", foreground="#2E5077", font=('Helvetica', 10, 'bold'))
        # self.style.configure('TButtonClicked', background="#2E5077", foreground="#F6F4F0", font=('Helvetica', 10, 'bold'))
        
        #Creating and packing frames 
        self.topFrame = tk.Frame(self.root, background="#79D7BE", height=100 )
        self.bottomFrame = tk.Frame(self.root, background="#4DA1A9")
        self.topFrame.pack(fill='x', pady=(0,10))
        self.bottomFrame.pack(fill='both', expand=True)
        
        #Image-control for bottom frame
        self.image_control = ImageControl(self.bottomFrame)
        
        #Chronological order
        self.file_operation = File(self.topFrame, self.bottomFrame, self.image_control, menubar, menu_font)
        self.edit_operation = Edit(self.topFrame, self.image_control, menubar, menu_font)
        self.custom_filters = CustomFilters(self.topFrame, self.image_control, menubar, custom_font, label_font, button_font, menu_font)
        self.graphs = Graphs(self.topFrame, self.image_control, menubar, menu_font)
        
        
        #adding image select
        # self.image_button = ttk.Button(self.topFrame, text="open image", command=self.image_control.on_image)
        # self.image_button.grid(row=0, column=0)
        # self.image_label = tk.Label(self.bottomFrame)
        # self.image_viewer = ImageViewer()
        
        #button icons
        # hand = Image.open("src/public/hand.png")
        # grab = Image.open("src/public/hold.png")
        # color = Image.open("src/public/color.jpg")
        # hand = hand.resize((50, 20), Image.LANCZOS)
        # grab = grab.resize((10, 10), Image.LANCZOS)
        hand_image = tk.PhotoImage("src/public/hand.png")
        # hand_image = hand_image.subsample(3, 3)

        #square buttons
        self.button_hand = ttk.Button(self.topFrame, image=hand_image, compound=tk.LEFT, command=self.image_control.toggle_drag)
        self.button_grab = ttk.Button(self.topFrame, image=hand_image, compound=tk.LEFT, command=self.image_control.toggle_drag).grid(row=1, column=3, ipadx=0, ipady=10)
        self.button_hand.bind("<Button-1>", self.button_color)
        self.button_hand.grid(row=1, column=0, ipadx=0, ipady=10)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        ttk.Button(self.topFrame, text="textOut", command=self.image_control.test_output).grid(row=1, column=1, ipadx=0, ipady=10)
        
        
    def on_closing(self):
        self.root.destroy() 
        sys.exit("Quiting..")
        
    def button_color(self, event):
        self.style.map("TButton", background=[("pressed", "#2E5077")])
        #self.button_hand.config(="#2E5077")
   