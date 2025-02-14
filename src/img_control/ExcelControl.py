import numpy as np

class ExcelControl:
    def __init__(self, image_control):
        self.image_control = image_control

    def value_thershold(self, lower, upper):
        try:
            pixel_array = self.image_control.get_image()
            pixel_array[pixel_array <= lower] = 0
            if upper != 0:
                pixel_array[pixel_array >= upper] = 0
            self.image_control.load_image(pixel_array)
            return True
        except Exception as e:
            print(f"ERROR IN value_threshold METHOD IN ExcelControl: \n{e}")
            return False
        
    def pixel_square(self):
        try:
            pixel_array = self.image_control.get_image()
            pixel_array = np.square(pixel_array)
            self.image_control.load_image(pixel_array)
        except Exception as e:
            print(e)

    def add_value_to_pixels(self, value: int, pixel_value: float):
        try:
            pixel_array = self.image_control.get_image()
            pixel_array[pixel_array >= pixel_value] += value
            self.image_control.load_image(pixel_array)
            return True
        except Exception as e:
            print(e)
            return False