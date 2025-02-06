#image loading and zoom in zoom out
import cv2
import tkinter as tk
from threading import Timer
from tkinter import filedialog
from PIL import Image, ImageTk
# import imageio as imageioFull
import imageio.v3 as imageio
from src.utils.customErrorBox import CustomErrorBox

class ImageControl:
    def __init__(self, root):
        self.root = root
        self.zoom_timer = None
        self.last_wheel_time = 0
        self.custom_error = CustomErrorBox(self.root)
        
        # Creating canvas widget
        self.canvas = tk.Canvas(self.root, bg="#4DA1A9")
        
        # Initialize image and image reference
        self.image = False
        self.tk_image = None
        self.photo = None
        self.drag = False
        
        # Image circular queue for undo redo options
        self.img_state = [None] * 10
        self.first = 0
        self.last = -1
        
        # Image position and scale tracking
        self.image_id = None
        self.image_x = 0
        self.image_y = 0
        self.height_scale = 1
        self.width_scale = 1
        
        # Binding mouse WHEEL for ZOOM in/out
        self.canvas.bind("<Button-4>", self.mouse_wheel)  # Linux
        self.canvas.bind("<Button-5>", self.mouse_wheel)  # Linux
        self.canvas.bind("<MouseWheel>", self.mouse_wheel)  # Windows
        
        # Minimum and maximum zoom levels
        self.MIN_SCALE = 0.1
        self.MAX_SCALE = 8.0
    
    def mouse_wheel(self, event):
        if not self.img_state[self.last]:
            return
            
        current_time = event.time
        if current_time - self.last_wheel_time < 200:
            return
        self.last_wheel_time = current_time
        
        try:
            if self.zoom_timer is not None:
                self.zoom_timer.cancel()
            
            if event.num == 5 or event.delta == -120:  # Zoom out
                self.zoom_timer = Timer(0.1, lambda: self.zoom_out())
            elif event.num == 4 or event.delta == 120:  # Zoom in
                self.zoom_timer = Timer(0.1, lambda: self.zoom_in())
            
            self.zoom_timer.start()
        except Exception as e:
            if self.zoom_timer:
                self.zoom_timer.cancel()
            self.custom_error.show("Error", str(e))

    def add_img_on_queue(self, image):
        try:
            size = len(self.img_state)
            if (self.last + 1) % size == self.first:
                self.last = (self.last + 1) % size
                self.first = (self.first + 1) % size
                self.img_state[self.last] = image.copy()  # Make a copy to prevent reference issues
            else:
                self.last = (self.last + 1) % size
                self.img_state[self.last] = image.copy()
                # Clear future states
                i = self.last
                while (i + 1) % size != self.first:
                    i = (i + 1) % size
                    self.img_state[i] = None
                
        except Exception as e:
            print(f"Error on circular queue: {e}")

    def load_image(self, image):
        self.canvas.pack(fill=tk.BOTH, expand=True)
        try:
            if image is not None:
                self.add_img_on_queue(image)
            elif self.img_state[self.last] is None:
                raise TypeError("No image available")
            
            current_image = self.img_state[self.last]
            photo = Image.fromarray(current_image)
            
            # Calculate new dimensions based on scale
            new_width = int(photo.width * self.width_scale)
            new_height = int(photo.height * self.height_scale)
            
            # Resize if needed
            if self.height_scale != 1:
                self.photo = photo.resize((new_width, new_height), Image.LANCZOS)
            else:
                self.photo = photo
            
            # Update display
            if self.tk_image:
                del self.tk_image  # Clean up old image
            self.tk_image = ImageTk.PhotoImage(self.photo)
            
            # Create or update image on canvas
            if self.image_id:
                self.canvas.itemconfig(self.image_id, image=self.tk_image)
            else:
                self.image_id = self.canvas.create_image(
                    self.image_x, self.image_y,
                    anchor=tk.NW,
                    image=self.tk_image
                )
            
        except Exception as e:
            self.tk_image = None
            self.custom_error.show("Error", f"Error in loading image: {str(e)}")

    def zoom_in(self):
        if self.img_state[self.last] is None:
            return
            
        new_scale = round(self.height_scale * 1.2, 2)
        if new_scale <= self.MAX_SCALE:
            self.height_scale = new_scale
            self.width_scale = new_scale
            self.load_image(None)  # Reload with new scale
        
    def zoom_out(self):
        if self.img_state[self.last] is None:
            return
            
        new_scale = round(self.height_scale * 0.8, 2)
        if new_scale >= self.MIN_SCALE:
            self.height_scale = new_scale
            self.width_scale = new_scale
            self.load_image(None)  # Reload with new scale

    def reset_view(self):
        """Reset zoom and position to default"""
        self.height_scale = 1
        self.width_scale = 1
        self.image_x = 0
        self.image_y = 0
        if self.img_state[self.last] is not None:
            self.load_image(None)

    # ... (keep other methods as they are) ...
