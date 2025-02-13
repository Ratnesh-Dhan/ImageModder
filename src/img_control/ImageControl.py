#image loading and zoom in zoom out
import cv2
import tkinter as tk
from threading import Timer
from tkinter import filedialog
from PIL import Image, ImageTk
# import imageio as imageioFull
import imageio.v3 as imageio
from src.utils.customErrorBox import CustomErrorBox
import pandas as pd
import numpy as np

class ImageControl:
    def __init__(self, root):
        self.root = root
        self.zoom_timer = None #  Timer for Debouncing zoom operation
        self.last_wheel_time = 0  # Initialize the wheel time tracker
        self.custom_error = CustomErrorBox(self.root)
        
        #creating canvas widget
        self.canvas = tk.Canvas(self.root, bg="#4DA1A9")
        # self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initialize image and image reference
        self.image = False
        self.tk_image = None
        self.photo = None
        self.drag = False
        # image circular queue for undo redo options
        self.img_state = [None]*10
        self.first = 0
        self.last = -1
        
        # # Image reference for draging Image
        self.image_id = None  # To keep track of the image on the canvas
        self.image_x = 0  # To track the x position of the image
        self.image_y = 0  # To track the y position of the image
        self.height_scale = 1
        self.width_scale = 1
        # self.dragging = False  # To track if the image is being dragged
        # self.last_x = 0  # Last x position of the mouse
        # self.last_y = 0  # Last y position of the mouse
        
        # # Binding mouse event for draging the image
        # self.canvas.bind("<ButtonPress-1>", self.start_drag)
        # self.canvas.bind("<B1-Motion>", self.do_drag)
        # self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        
        # Binding mouse WHEEL for ZOOM in/out
        # For linux OS
        self.canvas.bind("<Button-4>", self.mouse_wheel)
        self.canvas.bind("<Button-5>", self.mouse_wheel)
        # For windows OS
        self.canvas.bind("<MouseWheel>", self.mouse_wheel)
        
    def hide_widget(self):
        try:
            self.canvas.pack_forget()
        except Exception as e:
            self.custom_error.show("Caution", e)
        
    def undo(self):
        last = (self.last+(len(self.img_state)-1))%len(self.img_state)
        if self.img_state[last] is not None:
            print(self.last-self.first)
            if self.last - self.first != 1:
                self.last = last
                self.load_image(None)
    
    def redo(self):
        last = (self.last+1)%len(self.img_state)
        if (last != self.first) and (self.img_state[last] is not None):
            self.last = last
            self.load_image(None)
    
    def test_output(self):
        print(f"first: {self.first}, last: {self.last}")
        array = [1 if i is not None else 0 for i in self.img_state]
        array2 = [id(i) for i in self.img_state]
        print(array)
        print(array2)
        print(f"Instance id: {id(self.img_state[self.last])}")

    
    # def stop_drag(self, event):
    #     if self.drag:
    #         self.image_x = self.canvas.coords(self.image_id)[0]
    #         self.image_y = self.canvas.coords(self.image_id)[1]
        
    # def start_drag(self, event):
    #     if self.drag:
    #         self.last_x = event.x
    #         self.last_y = event.y
            
    # def do_drag(self, event):
    #     if self.drag:
    #         try:
    #             dx = event.x - self.last_x
    #             dy = event.y - self.last_y
    #             self.image_x = dx + self.image_x
    #             self.iamge_y = dy + self.image_y
    #             self.canvas.move(self.image_id, dx, dy)
    #             self.last_x = event.x
    #             self.last_y = event.y
    #         except Exception as e:
    #             print(f"something wrong with drag {e}")
       
    
    def mouse_wheel(self, event):
        current_time = event.time
        if current_time - self.last_wheel_time < 200: # 100ms threshold
            return
        self.last_wheel_time = current_time
        # print("scaling: ", self.height_scale)
        # respond to Linux or Windows wheel event
        try:
            if self.zoom_timer is not None:
                self.zoom_timer.cancel() #Cancel the previous timer
    
            if event.num == 5 or event.delta == -120:
                self.zoom_timer = Timer(0.1, self.zoom_out) #Delay for 100ms
            elif event.num == 4 or event.delta == 120:
                self.zoom_timer = Timer(0.1, self.zoom_in)
            self.zoom_timer.start()
        except RuntimeError:
            # Cancel all active timers
            if hasattr(self, 'zoom_timer') and self.zoom_timer is not None:
                self.zoom_timer.cancel()
        except Exception as e:
            self.custom_error.show("Error", e)

    def add_img_on_queue(self, image):
        try:
            size = len(self.img_state)
            if (self.last+1)%size == self.first:
                self.last = (self.last+1)%size
                self.first = (self.first+1)%size
                self.img_state[self.last] = image
            else:
                self.last = (self.last+1)%size
                self.img_state[self.last] = image
                i = self.last
                length = len(self.img_state)
                while((i+1)%length != self.first):
                    i = (i+1)%length
                    self.img_state[i] = None
                
            #print(f"first :{self.first}, last :{self.last}")   
                
        except Exception as e:
            print(f"error on circular queue :{e}")       
            
    def load_image(self, image):
        self.canvas.pack(fill=tk.BOTH, expand=True)         
        try:
            if image is not None:
                self.add_img_on_queue(image)             
            elif self.img_state[self.last] is None:
                #raise Exception("tk_image object is None")
                raise TypeError("tk_image object is type None")
                
            
            #self.photo = Image.fromarray(self.image)
            photo = Image.fromarray(self.img_state[self.last])
            if self.height_scale == 1:
                self.photo = photo
            else:
                self.photo = photo.resize((int(photo.width*self.width_scale), int(photo.height*self.height_scale)), Image.LANCZOS)
            # self.photo = Image.fromarray((self.img_state[self.last]).astype('uint8'))
            # self.photo = self.img_state[self.last]
            self.tk_image = ImageTk.PhotoImage(self.photo)
            #Display the image in the canvas
            self.canvas.image = self.tk_image
            self.image_id = self.canvas.create_image(self.image_x,self.image_y, anchor=tk.NW, image=self.canvas.image)
            
        except Exception as e:
            self.tk_image = None
            print(f"Error: {e}")
            #print(f"something went wrong {e}")
            self.custom_error.show("Error", f"Error in loading image: {e}")
    
    def open_excel(self):
        try:
            file_path = filedialog.askopenfilename(title="Select an Excel file", filetypes=[("Excel files", "*.xlsx;*.xls")])
        except Exception as e:
             print(f"Error on file path {e}")
             file_path = None
        if file_path:
            try:
                self.height_scale = 1
                self.width_scale = 1
                self.image_x = 0
                self.image_y = 0
                self.last=-1
                self.first=0
                self.img_state[:] = [None] * len(self.img_state)
                df = pd.read_excel(file_path, header=None) 
                pixel_array = df.to_numpy()
                pixel_array = pixel_array.astype(np.uint8)
                self.load_image(pixel_array)
            except Exception as e:
                self.custom_error.show("Error", f"faild to open excel: {e}")
                print(e)
        else:
            print("no filePath for excel")

    def on_image(self):
        try:
            file_path = filedialog.askopenfilename(title="select an image", filetypes=[("image", "*.png;*.jpg;*.bmp;*.jpeg")])
        except Exception as e:
             print(f"Error on file path {e}")
             file_path = None
        
        if file_path:
            try:
                self.height_scale = 1
                self.width_scale = 1
                self.image_x = 0
                self.image_y = 0
                self.last=-1
                self.first=0
                self.img_state[:] = [None] * len(self.img_state)
                image = imageio.imread(file_path)   
                self.load_image(image)
            except Exception as e:
                self.custom_error.show("Error", f"faild to open image: {e}")
                print(e)
        else:
            print("no filePath for image")
    
    def toggle_drag(self):
        try:
            if self.image_id is not None:
                self.drag = not self.drag
                return self.drag
            else:
                raise ValueError("ah.. I think you need to load an image first ;)")
        except ValueError as e:
            self.custom_error.show("Caution", e)
            
            
    def zoom_in(self, event=None):
        if self.image is not None:
            if self.height_scale > 8:
                return
            self.height_scale = round(self.height_scale * 1.2, 2)
            self.width_scale = round(self.width_scale * 1.2, 2)
            photo = Image.fromarray(self.img_state[self.last])
            self.photo = photo.resize((int(self.photo.width*1.2), int(self.photo.height*1.2)), Image.LANCZOS)
            del self.tk_image # deleting old image object to free up space
            self.tk_image = ImageTk.PhotoImage(self.photo)
            self.canvas.itemconfig(self.image_id, image=self.tk_image)
            # self.canvas.delete("all")
            # self.image_id = self.canvas.create_image(0,0 , anchor=tk.NW, image=self.tk_image)
        else:
            print("no image to zoom")
        
    def zoom_out(self, event=None):
        if self.image is not None:
            # self.photo = self.photo.resize((int(self.photo.width*0.8), int(self.photo.height*0.8)), Image.LANCZOS)
            self.width_scale = round(self.width_scale * 0.8, 2)
            self.height_scale = round(self.height_scale * 0.8, 2)
            photo = Image.fromarray(self.img_state[self.last])
            self.photo = photo.resize((int(self.photo.width*self.width_scale), int(self.photo.height*self.height_scale)), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.photo)
            self.canvas.itemconfig(self.image_id, image=self.tk_image)
            # self.canvas.delete("all")
            # self.image_id = self.canvas.create_image(0,0, anchor=tk.NW, image=self.tk_image)
        else:
            print("no image to zoom")
    
    def get_image(self):
        return self.img_state[self.last]
    
    def save_image(self):
        try:
            if self.img_state[self.last] is None:
                raise Exception("No image to save")
            else:
                print("in save")
                # Prompt the user to select a location to save the image
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
                
                # Save the image to the selected location
                print(file_path)
                if file_path:
                    imageio.imwrite(file_path, self.img_state[self.last])
                    self.custom_error.show("Sucess", "Saved...!")
        except Exception as e:
            self.custom_error.show("Error", e)
            print(e)
    
    def set_image(self, img):
        try:
            self.image = img
            return True
        except Exception as e:
            print(e)
            return False
        
    def rotate(self):
        img = self.img_state[self.last]
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        self.load_image(img)
        
    def xy(self):
        return self.image_x, self.image_y
    
    def set_xy(self, x, y):
        self.image_x = x
        self.image_y = y
    
    def get_scale(self):
        return self.height_scale, self.width_scale
    
    def reset_scale(self):
        self.height_scale = 1
        self.width_scale = 1
