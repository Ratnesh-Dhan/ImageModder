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
        self.window_form = None

    def toggle_select_boxes(self):
        try:
            if self.image_control.get_image() is not None:
                def apply_square_size():
                    self.square_size = int(entry1.get())
                    self.name = entry2.get()
                    self.toggle = True
                    self.image_control.canvas.bind("<Button-1>", self.click_to_cut_area)
                    self.window_form.destroy()
                    self.window_form = None

                if not self.toggle:

                    if self.window_form is not None and self.window_form.winfo_exists():
                        self.window_form.lift() # Bringing exsisting window form on top of screen
                    else:
                        self.window_form = tk.Toplevel(self.root)
                        self.window_form.title("Pixel Works")
                        window_width = 220
                        window_height = 150

                        #CENTERING THE WINDOW
                        screen_width = self.window_form.winfo_screenwidth()
                        screen_height = self.window_form.winfo_screenheight()
                        x = (screen_width//2) - (window_width // 2)
                        y = (screen_height // 2) - (window_height // 2)
                        self.window_form.geometry(f"{window_width}x{window_height}+{x}+{y}")

                        ttk.Label(self.window_form, text="Pixel Works", font=self.custom_font).pack()
                        # Sufixx for cut pieces 
                        frame2 = tk.Frame(self.window_form, padx=10, pady=5)
                        frame2.pack(fill='x')
                        ttk.Label(frame2, text='Name :').pack(side=tk.LEFT)
                        entry2 = ttk.Entry(frame2)
                        entry2.insert(0, "Square")
                        entry2.pack(side=tk.RIGHT, padx=(15, 5), pady=0)           
                        # Size of cut pieces as pixels
                        frame1 = tk.Frame(self.window_form, padx=10, pady=5 )
                        frame1.pack(fill='x')
                        ttk.Label(frame1, text="Square Size :").pack(side=tk.LEFT)
                        entry1 = ttk.Entry(frame1)
                        entry1.insert(0, "31")
                        entry1.focus()
                        entry1.pack(side=tk.RIGHT, padx=(15, 5), pady=0)
                        ttk.Button(self.window_form, text="Apply", command=apply_square_size).pack(pady=15 , ipadx=5, ipady=3)
                
                else:
                    self.unbind_select_boxes()
            else:
                self.custom_error.show("Error","No Image found.")
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
            # img = cv2.rectangle(self.image_control.get_image(), (x - (self.square_size//2 +1 ), y - (self.square_size//2 + 1 )), (x + 1 +  self.square_size//2, y + 1 + self.square_size//2), (0, 0, 255), 1)
            # cropped_img = img[y - self.square_size//2:y + self.square_size//2, x - self.square_size//2:x + self.square_size//2]
            # img = cv2.rectangle(self.image_control.get_image(),x_image + (x - (self.square_size//2 +1 ), y_image + y - (self.square_size//2 + 1 )),x_image + (x + 1 +  self.square_size//2, y_image + y + 1 + self.square_size//2), (0, 0, 255), 1)
            img = cv2.rectangle(self.image_control.get_image(), (x - (self.square_size//2 +1 ), y - (self.square_size//2 + 1 )), (x + 1 +  self.square_size//2, y + 1 + self.square_size//2), (0, 0, 255), 1)
            # cropped_img = img[y_image +y - self.square_size//2:y_image + y + self.square_size//2,x_image + x - self.square_size//2:x_image + x + self.square_size//2]
            cropped_img = img[y - self.square_size//2:y + self.square_size//2,x - self.square_size//2:x + self.square_size//2]
            
            self.image_control.load_image(img)

            # Converting the cropped image to BGR to RGB
            cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            # Save the cropped image
            output_dir = "squares"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            save_location = os.path.join(output_dir, f"{self.name}_{self.count}.png")
            if not os.path.exists(save_location):
                cv2.imwrite(save_location, cropped_img)
                self.count += 1
            else:
                while(os.path.exists(os.path.join(output_dir, f"{self.name}_{self.count}.png"))):   
                    self.count += 1
                cv2.imwrite(os.path.join(output_dir, f"{self.name}_{self.count}.png"), cropped_img)
                self.count += 1
        except Exception as e:
            self.custom_error.show("Error", str(e))



