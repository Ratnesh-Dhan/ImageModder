import cv2
import os
from src.utils.customErrorBox import CustomErrorBox

class PixelWorks:
    def __init__(self, root , image_control):
        self.root = root
        self.image_control = image_control
        self.pixel_work = None
        self.square_size = 21
        self.count = 0
        self.toggle = False
        self.custom_error = CustomErrorBox(self.root)

    def toggle_select_boxes(self):
        try:
            self.toggle = not self.toggle
            if self.toggle:
                self.image_control.canvas.bind("<Button-1>", self.click_to_cut_area)
            else:
                self.image_control.canvas.unbind("<Button-1>")
        except Exception as e:
            self.custom_error.show("Error", str(e))

    def unbind_select_boxes(self):
        try:
            self.image_control.canvas.unbind("<Button-1>")
            self.toggle = False
        except Exception as e:
            self.custom_error.show("Error", str(e))
    
    def click_to_cut_area(self, event):
        try:
            x, y = event.x, event.y
            img = cv2.rectangle(self.image_control.get_image(), (x - self.square_size//2, y - self.square_size//2), (x + self.square_size//2, y + self.square_size//2), (0, 0, 255), 1)
            cropped_img = img[y - self.square_size//2:y + self.square_size//2, x - self.square_size//2:x + self.square_size//2]
            self.image_control.load_image(img)

            # Save the cropped image
            output_dir = "squares"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            save_location = os.path.join(output_dir, f"square_{self.count}.png")
            if not os.path.exists(save_location):
                cv2.imwrite(save_location, cropped_img)
                self.count += 1
            else:
                while(os.path.exists(os.path.join(output_dir, f"square_{self.count}.png"))):
                    self.count += 1
                cv2.imwrite(os.path.join(output_dir, f"square_{self.count}.png"), cropped_img)
                self.count += 1
        except Exception as e:
            self.custom_error.show("Error", str(e))



