# # Class responsible for making selection on image and cut functionality on the selection
from src.utils.customErrorBox import CustomErrorBox
import cv2

# class ImageSelection:
#     def __init__(self,root, image_control):
#         self.height_scale, self.width_scale = image_control.get_scale()
#         self.image_control = image_control
#         self.image = None
#         self.start_x = None
#         self.start_y = None
#         self.cut_coords = None        
#         self.rect = None
#         self.canvas = self.image_control.canvas
        
#         self.messagebox = CustomErrorBox(root)
    
#     def __del__(self):
#         print("WARNING : Selection instance has been desolved.")
    
#     def start(self):
#         try:
#             self.image = self.image_control.get_image()
#             if self.image is not None:
#                 self.canvas.bind("<ButtonPress-1>", self.start_rectangle)
#                 self.canvas.bind("<B1-Motion>", self.draw_rectangle)
#                 self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)
#             else:
#                 raise ValueError("ah.. I think you need to load an image first ;)")
#         except ValueError as e:
#             self.messagebox.show("Caution", e)
#         except Exception as e:
#             self.messagebox.show("Error", e)
        
#     def start_rectangle(self, event):
#         self.start_x = event.x
#         self.start_y = event.y
#         if self.rect:
#             self.canvas.delete(self.rect)
#         self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
        
#     def draw_rectangle(self, event):
#         self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
#     def end_rectangle(self, event):
#         end_x, end_y = event.x, event.y
#         self.cut_coords = (self.start_x, self.start_y, end_x, end_y)
#         #THIS IS OUR TEST
#         print(f"this is rectangle coordinates: {self.cut_coords}")
        
#     def cut_image(self):
#         print("image actual 0,0:", self.image_control.image_x, self.image_control.image_y)
#         og_x = self.image_control.image_x
#         og_y = self.image_control.image_y
#         try:
#             def negetive_scaling(scale):
#                 og_scale = 1
#                 while scale != int(scale):
#                     scale = scale * 10
#                     og_scale = og_scale * 1
#                 return og_scale
#             if self.cut_coords:
#                 start_x, start_y, end_x, end_y = self.cut_coords
#                 height_scale, width_scale = self.image_control.get_scale()
#                 print("actual scale :", height_scale, width_scale)
#                 # Ensure coordinates are within image bounds
#                 # start_x = int(max(0, min(start_x, self.image.shape[1])) + og_x)
#                 # start_y = int(max(0, min(start_y, self.image.shape[0])) + og_y)
#                 # end_y = int(max(0, min(end_y, self.image.shape[0])) + og_y)
#                 # end_x = int(max(0, min(end_x, self.image.shape[1])) + og_x)
                
#                 # start_x = max(0, min(start_x, og_x)) 
#                 # start_y = max(0, min(start_y, og_y)) 
#                 # end_x = max(0, min(end_x, og_x)) 
#                 # end_y = max(0, min(end_y, og_y)) 
#                 if self.height_scale < 1:
#                     print("negetive scaling is working")
#                     og_scale = negetive_scaling(self.height_scale)
                    
#                     normalized_start_x = start_x / width_scale
#                     normalized_start_y = start_y / height_scale
#                     normalized_end_x = end_x / width_scale
#                     normalized_end_y = end_y / height_scale
#                     # normalized_start_x = start_x - og_x
#                     # normalized_start_y = start_y - og_y
#                     # normalized_end_x = end_x - og_x
#                     # normalized_end_y = end_y - og_y
                    
#                     start_x = int((normalized_start_x/width_scale) + og_x)
#                     start_y = int((normalized_start_y/height_scale) + og_y)
#                     end_x = int((normalized_end_x/width_scale) + og_x)
#                     end_y = int((normalized_end_y/height_scale) + og_y)
#                 else:
#                     #og is positiion of original image and start_x/y are position of rectangle . 
#                     #We are substracting og to match the position of the image by making it 
#                     #look like the image is at postion (0,0)
#                     start_x = int((start_x/self.width_scale) - (og_x/self.width_scale))
#                     start_y = int((start_y/self.height_scale) - (og_y/self.height_scale))
#                     end_x = int((end_x/self.width_scale) - (og_x/self.width_scale))
#                     end_y = int((end_y/self.height_scale) - (og_y/self.height_scale))
#                 print("coords during cut: ", start_x, start_y, end_x, end_y)
#                 # #THIS IS TESTING
#                 # test_image = self.image
#                 # cv2.rectangle(test_image, (start_x, start_y), (end_x, end_y), (0, 0, 255) , 3)
#                 # cv2.imshow("happy", test_image)
#                 # cv2.waitKey(0)
#                 # cv2.destroyAllWindows()
#                 # #/THIS IS TESTING
#                 # Crop the image
#                 cropped_image = self.image[start_y:end_y, start_x:end_x]
#                 # self.image_control.reset_scale()
#                 self.image_control.load_image(cropped_image)  
#                 self.canvas.delete(self.rect)
#             else:
#                 raise ValueError("No selection found. please select area before Cut function.")
#         except ValueError as e:
#             self.messagebox.show("Caution", e)
#         except Exception as e:
#             self.messagebox.show("Error", e)
            
#     def clean_up(self):
#         print("shit cleaning")
#         if self.rect:
#             self.canvas.delete(self.rect)
        
        
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
    
    def __del__(self):
        print("WARNING: Selection instance has been dissolved.")
    
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
            outline='red'
        )
        
    def draw_rectangle(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
    def end_rectangle(self, event):
        end_x, end_y = event.x, event.y
        self.cut_coords = (self.start_x, self.start_y, end_x, end_y)
        
    def convert_preview_to_original_coords(self, preview_x, preview_y):
        """Convert coordinates from preview image space to original image space"""
        height_scale, width_scale = self.image_control.get_scale()
        
        # Calculate relative position in the preview image
        relative_x = preview_x - self.image_control.image_x
        relative_y = preview_y - self.image_control.image_y
        
        # Convert to original image coordinates
        # For both zoom in and out, we divide by scale to get original coordinates
        original_x = int(relative_x / width_scale)
        original_y = int(relative_y / height_scale)
        
        return original_x, original_y
    
    def cut_image(self):
        try:
            if not self.cut_coords:
                raise ValueError("No selection found. Please select an area before cutting.")
                
<<<<<<< HEAD
            if self.image is None:
                raise ValueError("No image loaded.")
            
            # Get current scale
            height_scale, width_scale = self.image_control.get_scale()
                
            # Get the selection coordinates in preview space
            start_x, start_y, end_x, end_y = self.cut_coords
            
            # Print debug info
            print(f"Preview coordinates: ({start_x}, {start_y}) to ({end_x}, {end_y})")
            print(f"Image position: ({self.image_control.image_x}, {self.image_control.image_y})")
            print(f"Scale: (width: {width_scale}, height: {height_scale})")
            
            # Convert preview coordinates to original image coordinates
            orig_start_x, orig_start_y = self.convert_preview_to_original_coords(start_x, start_y)
            orig_end_x, orig_end_y = self.convert_preview_to_original_coords(end_x, end_y)
            
            # Print converted coordinates
            print(f"Original coordinates: ({orig_start_x}, {orig_start_y}) to ({orig_end_x}, {orig_end_y})")
            
            # Ensure coordinates are in the correct order (top-left to bottom-right)
            orig_start_x, orig_end_x = min(orig_start_x, orig_end_x), max(orig_start_x, orig_end_x)
            orig_start_y, orig_end_y = min(orig_start_y, orig_end_y), max(orig_start_y, orig_end_y)
            
            # Ensure coordinates are within image bounds
            img_height, img_width = self.image.shape[:2]
            orig_start_x = max(0, min(orig_start_x, img_width))
            orig_start_y = max(0, min(orig_start_y, img_height))
            orig_end_x = max(0, min(orig_end_x, img_width))
            orig_end_y = max(0, min(orig_end_y, img_height))
            
            # Print final cropping coordinates
            print(f"Final crop coordinates: ({orig_start_x}, {orig_start_y}) to ({orig_end_x}, {orig_end_y})")
            
            # Crop the image using the converted coordinates
            cropped_image = self.image[orig_start_y:orig_end_y, orig_start_x:orig_end_x]
            
            if cropped_image.size == 0:
                raise ValueError("Invalid selection area. Please try again.")
                
            # Update the image in the image control
            self.image_control.load_image(cropped_image)
            self.canvas.delete(self.rect)
            self.cut_coords = None
            
=======
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
                # Crop the image
                cropped_image = self.image[start_y:end_y, start_x:end_x]
                # self.image_control.reset_scale()
                self.image_control.load_image(cropped_image)  
                self.canvas.delete(self.rect)
            else:
                raise ValueError("No selection found. please select area before Cut function.")
>>>>>>> 1c74bdc2f4e7734bf8890101f9dad57cf083da6f
        except ValueError as e:
            self.messagebox.show("Caution", str(e))
        except Exception as e:
            self.messagebox.show("Error", f"An error occurred while cutting: {str(e)}")
            
    def clean_up(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.cut_coords = None