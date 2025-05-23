class PixelWorks:
    def __init__(self, root , image_control):
        self.root = root
        self.image_control = image_control
        self.pixel_work = None

    def click_to_cut_area(self):
        print("pixel work")
        def on_click(event):
            # Get the click coordinates relative to the canvas
            click_x = event.x
            click_y = event.y
            
            # Get the image position and scale
            image_x, image_y = self.image_control.xy()
            height_scale, width_scale = self.image_control.get_scale()
            
            # Convert click coordinates to original image coordinates
            relative_x = click_x - image_x
            relative_y = click_y - image_y
            
            # Convert to original image coordinates by dividing by scale
            original_x = int(relative_x / width_scale)
            original_y = int(relative_y / height_scale)
            print("--------------------------------")
            print(f"Click coordinates: ({click_x}, {click_y})")
            print(f"Image position: ({image_x}, {image_y})")
            print(f"Scale: (width: {width_scale}, height: {height_scale})")
            print(f"Original image coordinates: ({original_x}, {original_y})")
            print("--------------------------------")
            
            # Bind the click event to the canvas
            self.image_control.canvas.bind("<Button-1>", on_click)
        on_click()