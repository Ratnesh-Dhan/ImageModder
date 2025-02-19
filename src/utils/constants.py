from tkinter import font
from PIL import Image, ImageTk

def initialize_fonts():
    custom_font = font.Font(size=10,weight=font.BOLD, family='Comic Sans MS')
    #self.label_font = tk.font.Font(weight=font.BOLD, family="Helvetica")
    label_font = font.Font(family='Segoe UI')
    button_font = font.Font(family='Segoe UI Emoji')
    menu_font = font.Font(size=12, family='Corbel')
    return custom_font, label_font, button_font, menu_font

# button_bg = ?
# menu_bg = '#F6F4F0'
menu_bg = "#EBE5C2"
top_bg_color = "#504B38"
bottom_bg_color= "#B9B28A"

