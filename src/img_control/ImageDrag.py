class ImageDrag:
    def __init__(self, image_control):
        self.image_control = image_control
        self.canvas = image_control.canvas
        self.drag = None
        self.image_id = None
        self.image_x = 0
        self.image_y = 0
        self.dragging = False
        self.last_x = 0
        self.last_y = 0
        
        # Add boundaries for dragging
        self.MIN_X = -1000  # Adjust these values based on your needs
        self.MAX_X = 1000
        self.MIN_Y = -1000
        self.MAX_Y = 1000
    
    def stopu(self): 
        self.drag = None
        self.image_id = None
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    
    def start(self):
        self.drag = self.image_control.drag
        self.image_id = self.image_control.image_id
        self.image_x, self.image_y = self.image_control.xy()
        
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
    
    def stop_drag(self, event):
        if self.drag:
            try:
                coords = self.canvas.coords(self.image_id)
                if coords:  # Check if coords exists
                    self.image_x = coords[0]
                    self.image_y = coords[1]
                    self.image_control.set_xy(self.image_x, self.image_y)
            except Exception as e:
                print(f"Error in stop_drag: {e}")
        
    def start_drag(self, event):
        if self.drag:
            self.last_x = event.x
            self.last_y = event.y
            self.dragging = True
            
    def do_drag(self, event):
        if self.drag and self.dragging:
            try:
                # Calculate movement
                dx = event.x - self.last_x
                dy = event.y - self.last_y
                
                # Calculate new position
                new_x = self.image_x + dx
                new_y = self.image_y + dy
                
                # Apply boundaries
                new_x = max(self.MIN_X, min(self.MAX_X, new_x))
                new_y = max(self.MIN_Y, min(self.MAX_Y, new_y))
                
                # Calculate actual movement after boundaries
                actual_dx = new_x - self.image_x
                actual_dy = new_y - self.image_y
                
                # Update position
                self.image_x = new_x
                self.image_y = new_y
                self.canvas.move(self.image_id, actual_dx, actual_dy)
                
                # Update last position
                self.last_x = event.x
                self.last_y = event.y
                
            except Exception as e:
                print(f"Error in do_drag: {e}")
                self.dragging = False
