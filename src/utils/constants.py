from tkinter import font
from PIL import Image, ImageTk

def initialize_fonts():
    custom_font = font.Font(size=10,weight=font.BOLD, family='Comic Sans MS')
    #self.label_font = tk.font.Font(weight=font.BOLD, family="Helvetica")
    label_font = font.Font(family='Segoe UI')
    button_font = font.Font(family='Segoe UI Emoji')
    menu_font = font.Font(size=12, family='Corbel')
    return custom_font, label_font, button_font, menu_font

menu_bg = '#F6F4F0'

