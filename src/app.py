import sys
import os
import tkinter as tk
from tkinter import ttk
#from src.utils.image_utils import ImageViewer
from src.img_control.ImageControl import ImageControl
from src.img_control.ImageDrag import ImageDrag
from src.img_control.ImageSelection import ImageSelection
from src.img_control.PixelWorks import PixelWorks
from src.functions.filters import CustomFilters
from src.utils.customErrorBox import CustomErrorBox
from src.functions.graphs import Graphs
from src.functions.file import File
from src.functions.edit import Edit
from src.functions.excelOperation import ExcelOperation
from src.utils.constants import top_bg_color, bottom_bg_color
from PIL import Image, ImageTk

class App:
    def __init__(self, root, menubar, custom_font, label_font, button_font, menu_font):

        self.root = root
        self.root.title("ImageModder")
        
        width = root.winfo_width() + 800
        height = root.winfo_height() + 500
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.root.update_idletasks()
        # self.root.geometry("800x500")
        self.root.config(bg=top_bg_color)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.drag = False
        
        self.style = ttk.Style(root)
        # self.style.configure('TButton', background="#F6F4F0", foreground="#2E5077", font=('Helvetica', 10, 'bold'))
        # self.style.configure('TButtonClicked', background="#2E5077", foreground="#F6F4F0", font=('Helvetica', 10, 'bold'))
        
        #Creating and packing frames 
        self.topFrame = tk.Frame(self.root, background=top_bg_color, height=100 )
        self.bottomFrame = tk.Frame(self.root, background=bottom_bg_color)
        self.topFrame.pack(fill='x', pady=(0,10))
        self.bottomFrame.pack(fill='both', expand=True)
        
        #Image-control for bottom frame
        self.message = CustomErrorBox(self.root)
        self.image_control = ImageControl(self.bottomFrame)
        self.image_drag = ImageDrag(self.image_control)
        self.pixel_works = PixelWorks(self.root, self.image_control, custom_font)
        # self.image_selection = ImageSelection(self.bottomFrame, self.image_control)
        self.image_selection = None
        
        #Chronological order
        self.file_operation = File(self.topFrame, self.bottomFrame, self.image_control, menubar, menu_font)
        self.edit_operation = Edit(self.topFrame, self.bottomFrame, self.image_control, menubar, menu_font)
        self.custom_filters = CustomFilters(self.topFrame, self.image_control, menubar, custom_font, label_font, button_font, menu_font)
        self.graphs = Graphs(self.topFrame, self.image_control, menubar, menu_font)
        self.excel = ExcelOperation(self.topFrame, menubar, menu_font,custom_font,label_font, self.image_control)
        
        #button icons
        if getattr(sys, 'frozen', False):
            BASE_DIR = sys._MEIPASS
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        try:
            hand_path = os.path.join(BASE_DIR, "src", "public", "hand.png")
            hold_path = os.path.join(BASE_DIR,"src", "public", "hold.png")
            rotate_path = os.path.join(BASE_DIR, "src", "public", "rotate.png")
            select_path = os.path.join(BASE_DIR, "src", "public", "select.png")
            cut_path = os.path.join(BASE_DIR, "src", "public", "cut.png")
            pixel_path = os.path.join(BASE_DIR, "src", "public", "dot-square.png")
            hand_path = os.path.normpath(hand_path)
            hold_path = os.path.normpath(hold_path)
            rotate_path = os.path.normpath(rotate_path)
            select_path = os.path.normpath(select_path)
            cut_path = os.path.normpath(cut_path)
            pixel_path = os.path.normpath(pixel_path)
            hand = Image.open(hand_path)
            grab = Image.open(hold_path)
            rotate = Image.open(rotate_path)
            select = Image.open(select_path)
            cut = Image.open(cut_path)
            pixel = Image.open(pixel_path)
        except FileNotFoundError:
            hand = Image.open(os.path.normpath(os.path.join(BASE_DIR, "public", "hand.png")))
            grab = Image.open(os.path.normpath(os.path.join(BASE_DIR, "public", "hold.png")))
            rotate = Image.open(os.path.normpath(os.path.join(BASE_DIR, "public", "rotate.png")))
            select = Image.open(os.path.normpath(os.path.join(BASE_DIR, "public", "select.png")))
            cut = Image.open(os.path.normpath(os.path.join(BASE_DIR, "public", "cut.png")))
            pixel = Image.open(os.path.normpath(os.path.join(BASE_DIR, "public", "dot-square.png")))
        hand = hand.resize((30, 30), Image.LANCZOS)
        grab = grab.resize((30, 30), Image.LANCZOS)
        rotate = rotate.resize((30, 30), Image.LANCZOS)
        select = select.resize((30, 30), Image.LANCZOS)
        cut = cut.resize((30, 30), Image.LANCZOS)
        pixel = pixel.resize((30, 30), Image.LANCZOS)
        self.hand_image = ImageTk.PhotoImage(hand)
        self.grab_image = ImageTk.PhotoImage(grab)
        self.rotate_image = ImageTk.PhotoImage(rotate)
        self.select_image = ImageTk.PhotoImage(select)
        self.cut_image = ImageTk.PhotoImage(cut)
        self.pixel_image = ImageTk.PhotoImage(pixel)
        #square buttons
        self.button_hand = ttk.Button(self.topFrame, image=self.hand_image, command=self.drag_function)
        self.button_hand.bind("<Button-1>", self.button_color)
        self.button_hand.grid(row=1, column=0, ipady=2, ipadx=2)  
        ttk.Button(self.topFrame, image=self.rotate_image, command=self.rotate_the_image).grid(row=1, column=1, ipadx=2, ipady=2)  
        ttk.Button(self.topFrame, image=self.select_image, command=self.selection_start).grid(row=1, column=2, ipadx=2, ipady=2)  
        ttk.Button(self.topFrame, image=self.cut_image, command=self.image_cut).grid(row=1, column=3, ipadx=2, ipady=2)  
        ttk.Button(self.topFrame, image=self.pixel_image, command=self.pixel_works_toggle).grid(row=1, column=4, ipadx=2, ipady=2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        # ttk.Button(self.topFrame, text="textOut", command=self.image_control.test_output).grid(row=1, column=1, ipadx=0, ipady=10)

    def rotate_the_image(self):
        if self.image_selection is not None:
            self.image_selection.clean_up()
        self.pixel_works.unbind_select_boxes()
        self.image_control.rotate()
        
    def pixel_works_toggle(self):
        if self.image_selection is not None:
            self.image_selection.clean_up()
        self.pixel_works.toggle_select_boxes()

    def selection_start(self):
        if self.drag:
            self.image_control.toggle_drag()
            self.button_hand.config(image=self.hand_image)
            self.pixel_works.unbind_select_boxes()
            self.image_drag.stopu()
        if self.image_selection is not None:
            self.image_selection.clean_up()
            del self.image_selection
            self.image_selection = None
        self.image_selection = ImageSelection(self.bottomFrame, self.image_control)
        self.image_selection.start()
        
    def image_cut(self):
        try:
            self.image_selection.cut_image()
        except Exception:
            self.message.show("Caution", "Selection is required to cut image.")
        
    def drag_function(self):
        self.pixel_works.unbind_select_boxes()
        if self.image_selection is not None:
            # print("delete image_selection instnce from drag_function")
            self.image_selection.clean_up()
            del self.image_selection
            self.image_selection = None
        self.drag = self.image_control.toggle_drag()
        if self.drag:
            self.button_hand.config(image=self.grab_image)
            self.image_drag.start()    
        else:
            self.button_hand.config(image=self.hand_image)
            self.image_drag.stopu()
            
    def on_closing(self):
        self.root.destroy() 
        sys.exit("Quiting..")
        
    def button_color(self, event):
        self.style.map("TButton", background=[("pressed", "#2E5077")])
        #self.button_hand.config(="#2E5077")
   