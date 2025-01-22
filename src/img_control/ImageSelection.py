# Class responsible for making selection on image and cut functionality on the selection
from src.utils.customErrorBox import CustomErrorBox

class ImageSelection:
    def __init__(self,root, image_control):

        self.image_control = image_control
        self.image = None
        self.start_x = None
        self.start_y = None
        self.cut_coords = None        
        self.rect = None
        self.canvas = self.image_control.canvas
        
        self.messagebox = CustomErrorBox(root)
    
    def start(self):
        try:
            self.image = self.image_control.get_image()
            if self.image is not None:
                self.canvas.bind("<ButtonPress-1>", self.start_rectangle)
                self.canvas.bind("<B1-Motion>", self.draw_rectangle)
                self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)
            else:
                raise ValueError("ah.. I think you need to load an image first ;)")
        except ValueError as e:
            self.messagebox.show("Caution", e)
        except Exception as e:
            self.messagebox.show("Error", e)
        
    def start_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
        
    def draw_rectangle(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
    def end_rectangle(self, event):
        end_x, end_y = event.x, event.y
        self.cut_coords = (self.start_x, self.start_y, end_x, end_y)
        
    def cut_image(self):
        try:
            if self.cut_coords:
                start_x, start_y, end_x, end_y = self.cut_coords
                # Ensure coordinates are within image bounds
                start_x = max(0, min(start_x, self.image.shape[1]))
                start_y = max(0, min(start_y, self.image.shape[0]))
                end_x = max(0, min(end_x, self.image.shape[1]))
                end_y = max(0, min(end_y, self.image.shape[0]))
        
                # Crop the image
                cropped_image = self.image[start_y:end_y, start_x:end_x]
                self.image_control.load_image(cropped_image)  
                self.canvas.delete(self.rect)
            else:
                raise ValueError("No selection found. please select area before Cut function.")
        except ValueError as e:
            self.messagebox.show("Caution", e)
        except Exception as e:
            self.messagebox.show("Error", e)
        