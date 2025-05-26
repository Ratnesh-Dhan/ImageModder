import cv2
import os
from src.utils.customErrorBox import CustomErrorBox
import tkinter as tk
from tkinter import ttk

class PixelWorks:
    def __init__(self, root , image_control, custom_font):
        self.root = root
        self.image_control = image_control
        self.pixel_work = None
        self.square_size = 31
        self.name = "Square"
        self.count = 0
        self.toggle = False
        self.custom_error = CustomErrorBox(self.root)
        self.custom_font = custom_font

    def toggle_select_boxes(self):
        try:
            if not self.toggle:
                new_window = tk.Toplevel(self.root)
                new_window.title("Pixel Works")
                window_width = 220
                window_height = 150

                #CENTERING THE WINDOW
                screen_width = new_window.winfo_screenwidth()
                screen_height = new_window.winfo_screenheight()
                x = (screen_width//2) - (window_width // 2)
                y = (screen_height // 2) - (window_height // 2)
                new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

                ttk.Label(new_window, text="Pixel Works", font=self.custom_font).pack()
                
                frame2 = tk.Frame(new_window, padx=10, pady=5)
                frame2.pack(fill='x')
                ttk.Label(frame2, text='Name :').pack(side=tk.LEFT)
                entry2 = ttk.Entry(frame2)
                entry2.insert(0, "Square")
                entry2.pack(side=tk.RIGHT, padx=(15, 5), pady=0)
               

                frame1 = tk.Frame(new_window, padx=10, pady=5 )
                frame1.pack(fill='x')
                ttk.Label(frame1, text="Square Size :").pack(side=tk.LEFT)
                entry1 = ttk.Entry(frame1)
                entry1.insert(0, "31")
                entry1.focus()
                entry1.pack(side=tk.RIGHT, padx=(15, 5), pady=0)
                ttk.Button(new_window, text="Apply", command=lambda: print("hellow world")).pack(pady=15 , ipadx=5, ipady=3)

            self.toggle = not self.toggle
            if self.toggle:
                self.image_control.canvas.bind("<Button-1>", self.click_to_cut_area)
            else:
                self.image_control.canvas.unbind("<Button-1>")
        except Exception as e:
            self.custom_error.show("Error", str(e))

    def unbind_select_boxes(self):
        try:
            self.image_control.canvas.unbind("<Button-1>")
            self.toggle = False
        except Exception as e:
            self.custom_error.show("Error", str(e))
    
    def click_to_cut_area(self, event):
        try:
            x, y = event.x, event.y
            img = cv2.rectangle(self.image_control.get_image(), (x - (self.square_size//2 +1 ), y - (self.square_size//2 + 1 )), (x + 1 +  self.square_size//2, y + 1 + self.square_size//2), (0, 0, 255), 1)
            cropped_img = img[y - self.square_size//2:y + self.square_size//2, x - self.square_size//2:x + self.square_size//2]
            self.image_control.load_image(img)

            # Converting the cropped image to BGR to RGB
            cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            # Save the cropped image
            output_dir = "squares"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            save_location = os.path.join(output_dir, f"square_{self.count}.png")
            if not os.path.exists(save_location):
                cv2.imwrite(save_location, cropped_img)
                self.count += 1
            else:
                while(os.path.exists(os.path.join(output_dir, f"square_{self.count}.png"))):
                    self.count += 1
                cv2.imwrite(os.path.join(output_dir, f"square_{self.count}.png"), cropped_img)
                self.count += 1
        except Exception as e:
            self.custom_error.show("Error", str(e))



