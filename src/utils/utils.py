import matplotlib.pyplot as plt
from src.utils.customErrorBox import CustomErrorBox
import cv2

class Utils:
    def __init__(self, root):
        self.message = CustomErrorBox(root)
    
    def histogram(self, img):
        try:
            plt.hist(img.flatten())
            plt.show()
        except AttributeError as e:
            self.message.show("Error", e)

    def matplotlib_show(self, img):
        try:
            plt.title('By Matplotlib')
            plt.imshow(img, cmap="jet")
            plt.axis('off')
            plt.show()
        except Exception as e:
            self.message.show("error", e)
            print(e)
            
    def rgb_channel(self, img, val):
        try:
            if img is None:
                raise Exception("No image")
            else:
                if img.ndim != 3:  # Check if the image has color channels (3D array)
                    raise ValueError(f"The image does not have {val} color channel.")
                if val == 'all':
                    plt.close('all')
                    plt.subplot(1, 3, 1)
                    plt.imshow(img[:,:, 0], cmap='gray')
                    plt.title("red channel")
    
                    plt.subplot(1,3,2)
                    plt.imshow(img[:, :, 1], cmap='gray')
                    plt.title("green channel")
    
                    plt.subplot(1,3,3)
                    plt.imshow(img[:, :, 2], cmap='gray')
                    plt.title("blue channel")
                elif val == 'Red':
                    plt.title("red channel")
                    plt.imshow(img[:,:, 0], cmap='gray')
    
                elif val == 'Green':
                    plt.title("Green channel")
                    plt.imshow(img[:,:, 1], cmap='gray')
    
                elif val == 'Blue':
                    plt.title("Blue channel")
                    plt.imshow(img[:,:, 2], cmap='gray')
                else:
                    raise Exception(f"{val} option does not exists.")
                plt.show()
                
        except Exception as e:
            self.message.show("Error", e)

    def fit_to_screen(self, image_control, bottomFrame):
        try:
            img = image_control.get_image()
            image_control.reset_scale()
            if img is not None:
                screen_height = bottomFrame.winfo_height()
                print("Screen height: ", screen_height)
                print("Image height: ", img.shape[0])
                ratio = screen_height / img.shape[0]
                new_image = cv2.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio)))
                image_control.load_image(new_image)
            else:
                raise ValueError("The image is not loaded. Please load an image before processing.")
        except ValueError as e:
            self.message.show("Error", e)
        except Exception as e:
            self.message.show("Error", e)
            