from src.utils.utils import Utils
import tkinter as tk
from src.utils.constants import menu_bg

class Graphs:
    def __init__(self, root, image_control, menubar, menu_font):
        self.root = root
        self.utils = Utils(self.root)
        
        self.graph_menu = tk.Menu(menubar, tearoff=0)
        self.graph_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label="Show", menu=self.graph_menu)
        # self.graph_menu.add_command(label="Matplotlib show", command=lambda: self.utils.matplotlib_show(image_control.get_image()))
        self.graph_menu.add_command(label='Red Channel', command=lambda: self.utils.rgb_channel(image_control.get_image(), "Red"))
        self.graph_menu.add_command(label='Green Channel', command=lambda: self.utils.rgb_channel(image_control.get_image(), "Green"))
        self.graph_menu.add_command(label='Blue Channel', command=lambda: self.utils.rgb_channel(image_control.get_image(), "Blue"))
        self.graph_menu.add_command(label='View all Channel', command=lambda: self.utils.rgb_channel(image_control.get_image(), "all"))
        self.graph_menu.add_separator()
        self.graph_menu.add_command(label='Histogram', command=lambda: self.utils.histogram(image_control.get_image()))