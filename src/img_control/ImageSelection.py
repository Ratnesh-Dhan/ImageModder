from src.utils.customErrorBox import CustomErrorBox

class ImageSelection:
    def __init__(self, root, image_control):
        self.image_control = image_control
        self.image = None
        self.start_x = None
        self.start_y = None
        self.cut_coords = None        
        self.rect = None
        self.canvas = self.image_control.canvas
        self.messagebox = CustomErrorBox(root)
    
    def convert_preview_to_original_coords(self, preview_x, preview_y):
        """
        Convert preview coordinates to original image coordinates
        Accounting for both image position and scaling
        """
        height_scale, width_scale = self.image_control.get_scale()
        image_x, image_y = self.image_control.xy()
        
        # Step 1: Subtract image position to get relative coordinates
        relative_x = preview_x - image_x
        relative_y = preview_y - image_y
        
        # Step 2: Convert to original image coordinates
        # If scaled down, multiply by (1/scale)
        # If scaled up, divide by scale
        if width_scale < 1:
            original_x = int(relative_x * (1 / width_scale))
            original_y = int(relative_y * (1 / height_scale))
        else:
            original_x = int(relative_x / width_scale)
            original_y = int(relative_y / height_scale)
        
        return original_x, original_y
    
    def start(self):
        try:
            self.image = self.image_control.get_image()
            if self.image is not None:
                self.canvas.bind("<ButtonPress-1>", self.start_rectangle)
                self.canvas.bind("<B1-Motion>", self.draw_rectangle)
                self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)
            else:
                raise ValueError("Please load an image first!")
        except ValueError as e:
            self.messagebox.show("Caution", str(e))
        except Exception as e:
            self.messagebox.show("Error", str(e))
        
    def start_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 
            self.start_x, self.start_y, 
            outline='red', width=2
        )
        
    def draw_rectangle(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
    def end_rectangle(self, event):
        end_x, end_y = event.x, event.y
        self.cut_coords = (self.start_x, self.start_y, end_x, end_y)
        
    def cut_image(self):
        try:
            if not self.cut_coords:
                raise ValueError("No selection found. Please select an area before cutting.")
                
            if self.image is None:
                raise ValueError("No image loaded.")
            
            # Unpack selection coordinates
            start_x, start_y, end_x, end_y = self.cut_coords
            
            # Convert preview coordinates to original image coordinates
            orig_start_x, orig_start_y = self.convert_preview_to_original_coords(start_x, start_y)
            orig_end_x, orig_end_y = self.convert_preview_to_original_coords(end_x, end_y)
            
            # Ensure coordinates are in correct order
            x1, x2 = min(orig_start_x, orig_end_x), max(orig_start_x, orig_end_x)
            y1, y2 = min(orig_start_y, orig_end_y), max(orig_start_y, orig_end_y)
            
            # Validate selection against image dimensions
            img_height, img_width = self.image.shape[:2]
            x1 = max(0, min(x1, img_width))
            y1 = max(0, min(y1, img_height))
            x2 = max(0, min(x2, img_width))
            y2 = max(0, min(y2, img_height))
            
            # Debug prints to understand coordinate transformations
            print(f"Original Image Dimensions: {img_width}x{img_height}")
            print(f"Selection Coordinates: ({x1}, {y1}) to ({x2}, {y2})")
            
            # Validate selection size
            if x2 <= x1 or y2 <= y1:
                raise ValueError("Invalid selection area. Please try again.")
            
            # Crop the image
            cropped_image = self.image[y1:y2, x1:x2]
            
            if cropped_image.size == 0:
                raise ValueError("Selection resulted in zero-size image.")
            
            # Load cropped image
            self.image_control.load_image(cropped_image)
            
            # Clean up selection rectangle
            if self.rect:
                self.canvas.delete(self.rect)
            self.cut_coords = None
            
        except ValueError as e:
            self.messagebox.show("Caution", str(e))
        except Exception as e:
            self.messagebox.show("Error", f"Error during image cutting: {str(e)}")
    
    def clean_up(self):
        if self.rect:
            self.canvas.delete(self.rect)
        self.cut_coords = None