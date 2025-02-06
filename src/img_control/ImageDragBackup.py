# class handling image drag with hand icon

class ImageDrag:
    def __init__(self, image_control):
        self.image_control = image_control
        self.canvas = image_control.canvas
        self.drag = None
        
        # Image reference for draging Image
        self.image_id = None
        self.image_x = 0  # To track the x position of the image
        self.image_y = 0  # To track the y position of the image
        self.dragging = False  # To track if the image is being dragged
        self.last_x = 0  # Last x position of the mouse
        self.last_y = 0  # Last y position of the mouse
    
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
        # Binding mouse event for draging the image
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

            
    
    def stop_drag(self, event):
        if self.drag:
            try:
                self.image_x = self.canvas.coords(self.image_id)[0]
                self.image_y = self.canvas.coords(self.image_id)[1]
                self.image_control.set_xy(self.image_x, self.image_y)
            except Exception as e:
                print("Error: ", e)
        
    def start_drag(self, event):
        if self.drag:
            self.last_x = event.x
            self.last_y = event.y
            
    def do_drag(self, event):
        if self.drag:
            try:
                dx = event.x - self.last_x
                dy = event.y - self.last_y
                self.image_x = dx + self.image_x
                self.iamge_y = dy + self.image_y
                self.canvas.move(self.image_id, dx, dy)
                self.last_x = event.x
                self.last_y = event.y
            except Exception as e:
                print(f"something wrong with drag {e}")