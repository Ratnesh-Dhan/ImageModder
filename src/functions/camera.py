import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils.customErrorBox import CustomErrorBox
# import threading

class Camera:
    def __init__(self, top, bottom, image_control):
        self.top = top
        self.bottom = bottom
        self.image_control = image_control
        self.message = CustomErrorBox(self.top)
        self.label = tk.Label(self.bottom)
        self.label.pack()
        self.running = True
        self.capture = cv2.VideoCapture(0)
        self.update_frame()
        
        #Buttons for camera functions
        self.button = ttk.Button(self.top, text="Screenshot", command=self.take_screenshot)
        self.button.grid(row=1, column=3, ipadx=0, ipady=10)
    
    def __del__(self):
        self.stop()
        print("Camera instance closed")
        
    def update_frame(self):
        try:
            if self.running:
                ret, frame = self.capture.read()
                if ret:
                    cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2_im)
                    imagetk = ImageTk.PhotoImage(image=img)
                    self.label.config(image=imagetk)
                    self.label.image = imagetk
                self.bottom.update_idletasks()
                self.bottom.after(10, self.update_frame)
            
        except Exception as e:
            self.message.show("Error", e)
            
    def hide_widget(self):
        try:
            self.running = False
            self.capture.release()
            self.button.grid_forget()
            self.label.pack_forget()
        except Exception as e:
            print(e)
            self.message.show("Caution", e)
            
    def stop(self):
        self.running = False
        self.capture.release()
        
    def take_screenshot(self):
        try:
            ret, frame = self.capture.read()
            if ret:
                self.hide_widget()
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image_control.load_image(rgb_frame)

                del self
                # cv2.imwrite("Snapshot.png", rgb_frame)
                # self.message.show("Success", "Screenshot saved as screenshot.png")
        except Exception as e:
            self.message.show("Error", str(e))