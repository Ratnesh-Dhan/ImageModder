#filters
import cv2
from scipy import ndimage
import tkinter as tk
from tkinter import ttk
import numpy as np
from src.utils.customErrorBox import CustomErrorBox
from src.utils.constants import menu_bg

class CustomFilters:
    def __init__(self, frame, img_control, menubar, custom_font, label_font, button_font, menu_font):
         
        self.root = frame
        self.image_control = img_control
        
        self.custom_error = CustomErrorBox(self.root)
        
        #filter Menubar
        self.filter_menu = tk.Menu(menubar, tearoff=0)
        self.filter_menu.configure(bg=menu_bg, font=menu_font)
        menubar.add_cascade(label='Filters', menu=self.filter_menu)
        self.filter_menu.add_command(label='Gaussian', command=self.gaussian_filter)
        self.filter_menu.add_command(label='Median', command= self.median_filter)
        self.filter_menu.add_command(label='Average', command=self.average_filter)
        self.filter_menu.add_separator()
        self.filter_menu.add_command(label='Laplacian', command=self.laplace_filter)
        self.filter_menu.add_command(label='Sobel', command=self.sobel_filter)
        self.filter_menu.add_command(label='Prewitt', command=self.prewitt_filter)
        self.filter_menu.add_separator()
        self.filter_menu.add_command(label='Enhance Contrast', command=self.enhance_contrast)
        self.filter_menu.add_command(label='Sharpen', command= self.sharpen_filter)
        
        #Font 
        # self.custom_font = tk.font.Font(size=10,weight=tk.font.BOLD, family='Comic Sans MS')
        self.custom_font = custom_font
        self.label_font = label_font
        self.button_font = button_font
        #self.label_font = tk.font.Font(weight=tk.font.BOLD, family="Helvetica")
        # self.label_font = tk.font.Font(family='Segoe UI')
        # self.button_font = tk.font.Font(family='Segoe UI Emoji')
    def sharpen_filter(self):
        def sharpen_image(image):
            image = np.mean(image, axis=2).astype(np.uint8)
            # Define a sharpening kernel
            sharpening_kernel = np.array([[0, -1, 0],
                                          [-1, 5, -1],
                                          [0, -1, 0]])
            
            # Apply the sharpening filter using convolution
            sharpened = ndimage.convolve(image, sharpening_kernel, mode=combo1.get())
            
            # Normalize the result to the range [0, 255]
            sharpened -= sharpened.min()  # Shift to non-negative values
            sharpened *= 255.0 / sharpened.max()  # Normalize to [0, 255]
            sharpened = sharpened.astype(np.uint8)  # Convert to uint8
            
            return sharpened
        img = self.image_control.get_image()
        if img is not None:
            def apply_sharpen_filter():
                try:
                    image = img
                    # kernel = np.array([[-1, -1, -1],
                    #                   [-1, 9, -1],
                    #                   [-1, -1, -1]])
                    # new_image = ndimage.convolve(img, kernel, mode='nearest')
                    if image.ndim == 3:  # Check if the image has color channels
                        # image = np.mean(image, axis=2)  # Convert to grayscale by averaging the color channels
                        image = image.flatten()
                    # Ensure the image is in the correct format (2D)
                    image = image.astype(np.float32)  # Convert to float for processing
                    new_image = sharpen_image(image)
                    self.image_control.load_image(new_image)
                    new_window.destroy()
                except Exception as e:
                    self.custom_error.show("Error", e)

            new_window = tk.Toplevel(self.root)
            new_window.title("Sharpen Filter")
            new_window.geometry("220x150")
            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 220
            window_height = 150
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            ttk.Label(new_window, text="Sharpen", font=self.custom_font).pack()
            frame1 = tk.Frame(new_window, padx=10, pady=5 )
            frame1.pack()
            combo1 = ttk.Combobox(
                frame1,
                state='readonly',
                values=['reflect', 'constant', 'nearest', 'mirror', 'wrap']
                )
            combo1.set('reflect')
            combo1.grid(row=0, column=1)
            ttk.Label(frame1, text="Mode: ", font=self.label_font).grid(row=0, column=0)
            # combo1.grid(row=0, column=1)
            ttk.Button(new_window, text="Apply", command=apply_sharpen_filter).pack(pady=10, ipadx=5, ipady=3)
        else:
            self.custom_error.show("Error", "no image found")
            print("Error: no image found.")
            
    def prewitt_filter(self):
        img = self.image_control.get_image()
        def apply_prewitt_filter():
            try:
                # mode = combo1.get()
                # axis = int(entry1.get())
                # cval = float(entry2.get())
                # new_image = ndimage.prewitt(img, axis=axis, mode=mode, cval=cval)
                
                image = img
                if image.ndim == 3:  # Check if the image has color channels
                    image = np.mean(image, axis=2)  # Convert to grayscale by averaging the color channels
                
                # Define Prewitt filter kernels
                prewitt_x = np.array([[1, 0, -1],
                                      [1, 0, -1],
                                      [1, 0, -1]])
                
                prewitt_y = np.array([[1, 1, 1],
                                      [0, 0, 0],
                                      [-1, -1, -1]])
                
                # Apply the Prewitt filter
                dx = ndimage.convolve(image, prewitt_x)  # Horizontal derivative
                dy = ndimage.convolve(image, prewitt_y)  # Vertical derivative
                prewitt_magnitude = np.hypot(dx, dy)  # Magnitude
                prewitt_magnitude *= 255.0 / np.max(prewitt_magnitude)  # Normalize (Q&D)
                new_image = prewitt_magnitude.astype(np.uint8)  # Convert to uint8
                
                self.image_control.load_image(new_image)
                new_window.destroy()
            except Exception as e:
                print(f"Error: {e}")
                self.custom_error.show("Error", "e")
        if img is not None:
            new_window = tk.Toplevel(self.root)
            new_window.title("Prewitt Filter")
            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 210
            window_height = 220
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            ttk.Label(new_window, text="Prewitt Filter", font=self.custom_font).pack()
            frame1 = tk.Frame(new_window, padx=10, pady=5)
            frame1.pack()
            ttk.Label(frame1, text="Mode: ", font=self.label_font).grid(row=0, column=0)
            combo1 = ttk.Combobox(
                frame1,
                state='readonly',
                values=['reflect', 'constant', 'nearest', 'mirror', 'wrap']
                )
            combo1.set('reflect')
            combo1.grid(row=0, column=1)
            ttk.Label(new_window, text="..optionals..", font=('Arial', 10, 'italic')).pack()
            frame2 = tk.Frame(new_window, padx=10, pady=5)
            frame2.pack()
            ttk.Label(frame2, text="axis: ", font=self.label_font).grid(row=0, column=0, padx=(0, 20))
            entry1 = ttk.Entry(frame2)
            entry1.insert(0, '-1')
            entry1.grid(row=0, column=1)
            frame3 = tk.Frame(new_window, padx=10, pady=5)
            frame3.pack()
            ttk.Label(frame3, text="cval: ", font=self.label_font).grid(row=0, column=0, padx=(0, 20))
            entry2 = ttk.Entry(frame3)
            entry2.insert(0, "0.0")
            entry2.grid(row=0, column=1)
            ttk.Button(new_window, text="Apply", command=apply_prewitt_filter).pack( pady=10, ipadx=5, ipady=3)
        else:
            self.custom_error.show("Error","image not found")
            
    def sobel_filter(self):
        img = self.image_control.get_image()
        def apply_sobel_filter():
            try:
                mode = combo1.get()
                axis = combo2.get()
                # cval = float(entry2.get())
                # # new_image = ndimage.sobel(img, axis=1, mode=mode, cval=cval)
                # new_image = ndimage.sobel(img, 1)
                
                image = img
                if image.ndim == 3:  # Check if the image has color channels
                    image = np.mean(image, axis=2)  # Convert to grayscale by averaging the color channels

                if axis == 'x':
                    dx = ndimage.sobel(image, axis=0, mode=mode)  # horizontal derivative
                    mag = dx
                    # mag *= 255.0 / np.max(dx)  # normalize (Q&D)
                elif axis == 'y':
                    dy = ndimage.sobel(image, axis=1, mode=mode)  # vertical derivative
                    mag = dy
                    # mag *= 255.0 / np.max(dy)  # normalize (Q&D)
                    
                else:                    
                    dx = ndimage.sobel(image, axis=0, mode=mode)  # horizontal derivative
                    dy = ndimage.sobel(image, axis=1, mode=mode)  # vertical derivative
                    mag = np.hypot(dx, dy)  # magnitude
                    mag *= 255.0 / np.max(mag)  # normalize (Q&D)
                
                mag = mag.astype(np.uint8)
                
                
                self.image_control.load_image(mag)
                new_window.destroy()
            except Exception as e:
                print(f"Error: {e}")
                self.custom_error.show("Error", e)
        if img is not None:
            new_window = tk.Toplevel(self.root)
            new_window.title("Sobel Filter")

            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 210
            window_height = 220
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            ttk.Label(new_window, text="Sobel Filter", font=self.custom_font).pack()
            frame1 = tk.Frame(new_window, padx=10, pady=5)
            frame1.pack()
            ttk.Label(frame1, text="Mode: ", font=self.label_font).grid(row=0, column=0)
            combo1 = ttk.Combobox(
                frame1,
                state='readonly',
                values=['reflect', 'constant', 'nearest', 'mirror', 'wrap']
                )
            combo1.set('reflect')
            combo1.grid(row=0, column=1)
            ttk.Label(new_window, text="..optionals..", font=('Arial', 10, 'italic')).pack()
            frame2 = tk.Frame(new_window, padx=10, pady=5)
            frame2.pack()
            ttk.Label(frame2, text="axis: ", font=self.label_font).grid(row=0, column=0, padx=(0,10))
            combo2 = ttk.Combobox(
                frame2,
                state='readonly',
                values=['x', 'y', 'x & y']
                )
            combo2.set('x & y')
            combo2.grid(row=0, column=1)
            frame3 = tk.Frame(new_window, padx=10, pady=5)
            frame3.pack()
            ttk.Label(frame3, text="cval: ", font=self.label_font).grid(row=0, column=0, padx=(0, 20))
            entry2 = ttk.Entry(frame3)
            entry2.insert(0, "0.0")
            entry2.grid(row=0, column=1)
            ttk.Button(new_window, text="Apply", command=apply_sobel_filter).pack( pady=10, ipadx=5, ipady=3)
        else:
            self.custom_error.show("Caution","Image not found")
            
    def enhance_contrast(self):
        try:
            img = self.image_control.get_image()
            if img is not None:
                p2, p98 = np.percentile(img, (2, 98))  # Get the 2nd and 98th percentiles
                contrast_stretched = np.clip((img - p2) * (255 / (p98 - p2)), 0, 255)  # Stretch contrast
                contrast_stretched = contrast_stretched.astype(np.uint8)
                self.image_control.load_image(contrast_stretched)
            else:
                raise TypeError("No image found.!")
        except TypeError as e:
            self.custom_error.show("Caution", e)
        except Exception as e:
            self.custom_error.show("Error", e)
    
    def laplace_filter(self):
        img = self.image_control.get_image()
        def enhance_contrast(image):
            p2, p98 = np.percentile(image, (2, 98))  # Get the 2nd and 98th percentiles
            contrast_stretched = np.clip((image - p2) * (255 / (p98 - p2)), 0, 255)  # Stretch contrast
            return contrast_stretched.astype(np.uint8)
        
        def apply_laplace_filter():
            try:
                mode = combo1.get()
                cval = float(entry2.get())
                # new_image = ndimage.laplace(img, mode=mode, cval=cval)
                image = img
                if image.ndim == 3:  # Check if the image has color channels
                    image = np.mean(image, axis=2)  # Convert to grayscale by averaging the color channels
                
                # Apply the Laplacian filter
                laplacian = ndimage.laplace(image, mode=mode, cval=cval)
                
                # Normalize the result to the range [0, 255]
                laplacian = laplacian - np.min(laplacian)  # Shift to non-negative values
                laplacian = (laplacian / np.max(laplacian)) * 255.0  # Normalize to [0, 255]
                new_image = laplacian.astype(np.uint8)  # Convert to uint8
                
                #ENHANCING CONTRAST 
                #new_image = enhance_contrast(new_image)
                
                self.image_control.load_image(new_image)
                new_window.destroy()
            except Exception as e:
                print(f"Error: {e}")
                self.custom_error.show("Error", e)
        if img is not None:
            new_window = tk.Toplevel(self.root)
            new_window.title("Laplace Filter")
            
            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 210
            window_height = 180
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            ttk.Label(new_window, text="Laplace Filter", font=self.custom_font).pack()
            frame1 = tk.Frame(new_window, padx=10, pady=5)
            frame1.pack()
            ttk.Label(frame1, text="Mode: ", font=self.label_font).grid(row=0, column=0)
            combo1 = ttk.Combobox(
                frame1,
                state='readonly',
                values=['reflect', 'constant', 'nearest', 'mirror', 'wrap']
                )
            combo1.set('reflect')
            combo1.grid(row=0, column=1)
            ttk.Label(new_window, text="..optionals..", font=('Arial', 10, 'italic')).pack()
            frame3 = tk.Frame(new_window, padx=10, pady=5)
            frame3.pack()
            ttk.Label(frame3, text="cval: ", font=self.label_font).grid(row=0, column=0, padx=(0, 20))
            entry2 = ttk.Entry(frame3)
            entry2.insert(0, "0.0")
            entry2.grid(row=0, column=1)
            ttk.Button(new_window, text="Apply", command=apply_laplace_filter).pack( pady=10, ipadx=5, ipady=3)
        else:
            self.custom_error.show("Error", "No image found.!")
        
    def median_filter(self):
        print("median called")
        img = self.image_control.get_image()
        if img is not None:
            def apply_median_filter():
                try:
                    size = int(entry1.get())
                    mode = combo.get()
                    if size <= 0:
                        label1.config(text="size must be a positive integer")
                    else:
                          new_image = ndimage.median_filter(img, size=size, mode=mode)
                          self.image_control.load_image(new_image)
                          new_window.destroy()    
                except ValueError:
                   # custom_font = tk.font.Font(size=10, weight=tk.font.NORMAL, family="Arial", slant="italic")
                    label1.config(text="Invalid input. Please enter a positive integer.")
                
            new_window = tk.Toplevel(self.root)
            new_window.title("Median Filter")
            
            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 200
            window_height = 130
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            label1 = ttk.Label(new_window, text="Median Filter", font=self.custom_font)
            label1.pack()
            subFrame1 = tk.Frame(new_window)
            subFrame1.pack(fill='x')
            label2 = ttk.Label(subFrame1, text="Size :", font=self.label_font)
            label2.pack(side = tk.LEFT, padx=(15, 6), pady=0)
            entry1 = ttk.Entry(subFrame1)
            entry1.insert(0, "3")
            entry1.focus()
            entry1.pack(side = tk.RIGHT, padx=(5, 15), pady=0)
            subFrame2 = tk.Frame(new_window, padx=10, pady=5)
            subFrame2.pack()
            ttk.Label(subFrame2, text="Mode :", font=self.label_font).pack(side=tk.LEFT, padx=5, pady=0)
            combo = ttk.Combobox(
                subFrame2,
                state='readonly',
                values=['reflect', 'constant', 'nearest', 'mirror', 'wrap']
                )
            combo.set('reflect')
            combo.pack()
            ttk.Button(new_window, text="Apply", command=apply_median_filter).pack( pady=10 , ipadx=5, ipady=3)
        else:
            self.custom_error.show("Error", "No image found.!")
            print("Error: no image found.!")
        
    def gaussian_filter(self):
        print("gaussian called")
        img = self.image_control.get_image()
        if img is not None:
            def apply_gaussian_filter():
                try:
                    sigma = int(entry1.get())
                    mode = combo1.get()
                    if entry2.get() == "None":
                        axes = None
                    else:
                        axes = int(entry2.get())
                    cval = float(entry3.get())
                    truncate = float(entry4.get())
                    print(sigma, mode, axes, cval, truncate)
                    
                    new_image = ndimage.gaussian_filter(img, sigma=sigma, mode=mode, cval=cval, truncate=truncate, axes=axes)
                    self.image_control.load_image(new_image)
                    new_window.destroy()
                except ValueError as ve:
                    print(ve)
            new_window = tk.Toplevel(self.root)
            new_window.title("Gaussian filter")
            
            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 210
            window_height = 280
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            ttk.Label(new_window, text="Gaussian filter", font=self.custom_font).pack()
            frame1 = tk.Frame(new_window, padx=10, pady=5)
            frame1.pack()
            ttk.Label(frame1, text="Standard deviation :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            entry1 = ttk.Entry(frame1)
            entry1.insert(0, "1")
            entry1.focus()
            entry1.pack(side=tk.RIGHT)
            frame2 = tk.Frame(new_window, padx=10, pady=5)
            frame2.pack()
            ttk.Label(frame2, text="Mode :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            combo1 = ttk.Combobox(
                frame2,
                state='readonly',
                values=['reflect', 'constant', 'nearest', 'mirror', 'wrap']
                )
            combo1.set('reflect')
            combo1.pack()
            ttk.Label(new_window, text="..optionals..", font=('Arial', 10, 'italic')).pack()
            frame3 = tk.Frame(new_window, padx=10, pady=5)
            frame3.pack()
            ttk.Label(frame3, text="axes :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            entry2 = ttk.Entry(frame3)
            entry2.insert(0, "None")
            entry2.pack(side=tk.RIGHT)
            
            frame4 = tk.Frame(new_window, padx=10, pady=5)
            frame4.pack()
            ttk.Label(frame4, text="cval :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            entry3 = ttk.Entry(frame4)
            entry3.insert(0, "0.0")
            entry3.pack(side=tk.RIGHT)
            
            frame5 = tk.Frame(new_window, padx=10, pady=5)
            frame5.pack()
            ttk.Label(frame5, text="truncate :", font=self.label_font).pack(side=tk.LEFT, padx=(0,10))
            entry4 = ttk.Entry(frame5)
            entry4.insert(0, "4.0")
            entry4.pack(side=tk.RIGHT)
            
            ttk.Button(new_window, text="Apply", command=apply_gaussian_filter).pack( pady=10 , ipadx=5, ipady=3)
        else:
            self.custom_error.show("Error", "No image found")
            print("Error: no image found..!")
            
    def average_filter(self):
        print("average called")
        img = self.image_control.get_image()
        if img is not None:
            def apply_average_filter():
                try:
                    new_image = cv2.blur(img, (3,3))
                    self.image_control.load_image(new_image)
                    new_window.destroy()
                except Exception as e:
                    print(e)
            new_window = tk.Toplevel(self.root)
            new_window.title("Average Filter")
            
            #CENTERING THE WINDOW
            # Set the desired size of the window
            window_width = 200
            window_height = 100
            
            screen_width = new_window.winfo_screenwidth()
            screen_height = new_window.winfo_screenheight()
            x = (screen_width//2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            label = ttk.Label(new_window, text="Average Filter", font=self.custom_font)
            label.pack()
            frame1 = tk.Frame(new_window, padx=5, pady=5)
            frame1.pack()
            ttk.Label(frame1, text="Mask :",font=self.label_font).pack(side=tk.LEFT)
            entry1 = ttk.Entry(frame1)
            entry1.insert(0, "3")
            entry1.pack(side=tk.RIGHT)
            ttk.Button(new_window, text="Apply", command=apply_average_filter).pack(side=tk.BOTTOM, pady=(0, 10))
        else:
            self.custom_error.show("Error", "No image found")
            
    def average_backup(self):
        img = []
        
        #Starts from here
        m, n = img.shape 

        # Develop Averaging filter(3, 3) mask 
        mask = np.ones([3, 3], dtype = int) 
        mask = mask / 9
           
        # Convolve the 3X3 mask over the image  
        img_new = np.zeros([m, n]) 
          
        for i in range(1, m-1): 
            for j in range(1, n-1): 
                temp = img[i-1, j-1]*mask[0, 0]+img[i-1, j]*mask[0, 1]+img[i-1, j + 1]*mask[0, 2]+img[i, j-1]*mask[1, 0]+ img[i, j]*mask[1, 1]+img[i, j + 1]*mask[1, 2]+img[i + 1, j-1]*mask[2, 0]+img[i + 1, j]*mask[2, 1]+img[i + 1, j + 1]*mask[2, 2] 
                 
                img_new[i, j]= temp 
                  
        new_imageine = img_new.astype(np.uint8) 
        
        #End here
        return new_imageine