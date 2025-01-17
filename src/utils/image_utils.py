import imageio.v3 as imageio
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self):
        self.image = None
    
    def load_image(self, file_path):
        self.image = imageio.imread(file_path)
        return self.image
        
    def get_image(self):  
        if self.image is None:
            return None
        photo = Image.fromarray(self.image)
        return ImageTk.PhotoImage(photo)