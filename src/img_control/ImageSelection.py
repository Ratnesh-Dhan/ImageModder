# Class responsible for making selection on image and cut functionality on the selection
from src.utils.customErrorBox import CustomErrorBox
import cv2

class ImageSelection:
    def __init__(self,root, image_control):
        self.height_scale, self.width_scale = image_control.get_scale()
        print("this is scale from ImageSelection", self.height_scale, " : ", self.width_scale)
        self.image_control = image_control
        self.image = None
        self.start_x = None
        self.start_y = None
        self.cut_coords = None        
        self.rect = None
        self.canvas = self.image_control.canvas
        
        self.messagebox = CustomErrorBox(root)
    
    def __del__(self):
        print("WARNING : Selection instance has been desolved.")
    
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
        #THIS IS OUR TEST
        print(f"this is rectangle coordinates: {self.cut_coords}")
        
    def cut_image(self):
        print("image actual 0,0:", self.image_control.image_x, self.image_control.image_y)
        og_x = self.image_control.image_x
        og_y = self.image_control.image_y
        try:
            def negetive_scaling(scale):
                og_scale = 1
                while scale != int(scale):
                    scale = scale * 10
                    og_scale = og_scale * 1
                return og_scale
            if self.cut_coords:
                start_x, start_y, end_x, end_y = self.cut_coords
                # Ensure coordinates are within image bounds
                # start_x = int(max(0, min(start_x, self.image.shape[1])) + og_x)
                # start_y = int(max(0, min(start_y, self.image.shape[0])) + og_y)
                # end_y = int(max(0, min(end_y, self.image.shape[0])) + og_y)
                # end_x = int(max(0, min(end_x, self.image.shape[1])) + og_x)
                
                # start_x = max(0, min(start_x, og_x)) 
                # start_y = max(0, min(start_y, og_y)) 
                # end_x = max(0, min(end_x, og_x)) 
                # end_y = max(0, min(end_y, og_y)) 
                print(self.height_scale)
                if self.height_scale < 1:
                    print("negetive scaling is working")
                    og_scale = negetive_scaling(self.height_scale)
                    # start_x = int(og_scale*(start_x/self.width_scale) - og_scale*(og_x/self.width_scale))
                    # start_y = int(og_scale*(start_y/self.height_scale) - og_scale*(og_y/self.height_scale))
                    # end_x = int(og_scale*(end_x/self.width_scale) - og_scale*(og_x/self.width_scale))
                    # end_y = int(og_scale*(end_y/self.height_scale) - og_scale*(og_y/self.height_scale))
                    start_x = int(og_scale*(start_x/self.width_scale))
                    start_y = int(og_scale*(start_y/self.height_scale))
                    end_x = int(og_scale*(end_x/self.width_scale) - og_scale*(og_x/self.width_scale))
                    end_y = int(og_scale*(end_y/self.height_scale) - og_scale*(og_y/self.height_scale))
                else:
                    start_x = int((start_x/self.width_scale) - (og_x/self.width_scale))
                    start_y = int((start_y/self.height_scale) - (og_y/self.height_scale))
                    end_x = int((end_x/self.width_scale) - (og_x/self.width_scale))
                    end_y = int((end_y/self.height_scale) - (og_y/self.height_scale))
                print("coords during cut: ", start_x, start_y, end_x, end_y)
                #THIS IS TESTING
                test_image = self.image
                cv2.rectangle(test_image, (start_x, start_y), (end_x, end_y), (0, 0, 255) , 3)
                cv2.imshow("happy", test_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                #/THIS IS TESTING
                # Crop the image
                cropped_image = self.image[start_y:end_y, start_x:end_x]
                # self.image_control.reset_scale()
                self.image_control.load_image(cropped_image)  
                self.canvas.delete(self.rect)
            else:
                raise ValueError("No selection found. please select area before Cut function.")
        except ValueError as e:
            self.messagebox.show("Caution", e)
        except Exception as e:
            self.messagebox.show("Error", e)
            
    def clean_up(self):
        print("shit cleaning")
        if self.rect:
            self.canvas.delete(self.rect)
        
        