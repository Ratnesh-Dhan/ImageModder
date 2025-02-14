# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk

# class CustomErrorBox:
#     def __init__(self, root):
#         self.root = root
#         self.font = tk.font.Font(size=13, weight=tk.font.BOLD, family='Comic Sans MS')
        
#     def calculate_text_dimensions(self, message, max_width_pixels):
#         # Create a temporary Text widget to measure text dimensions
#         temp = tk.Text(self.root, font=self.font)
#         temp.pack()
        
#         # Insert message and configure wrapping
#         temp.insert(tk.END, message)
#         temp.config(width=max_width_pixels // self.font.measure('0'))  # Convert pixels to character width
        
#         # Get the bbox of the last character to determine total height
#         temp.see(tk.END)
#         last_pos = f"{temp.count('1.0', tk.END, 'lines')-1}.0"
#         bbox = temp.bbox(last_pos)
        
#         # Calculate required dimensions
#         width = min(temp.winfo_reqwidth(), max_width_pixels)
#         height = bbox[1] + bbox[3] if bbox else 50  # Height of last line + its y-position
        
#         # Clean up
#         temp.destroy()
        
#         return width, height
        
#     def show(self, title, message):
#         # Image handling
#         img_paths = {
#             'Caution': 'src/public/caution.png',
#             'Error': 'src/public/cancel.png',
#             'Success': 'src/public/checked.png'
#         }
#         img = img_paths.get(title, 'src/public/cancel.png')
        
#         photo = Image.open(img)
#         photo = photo.resize((50, 50))
#         photo = ImageTk.PhotoImage(photo)
        
#         # Create toplevel window
#         top = tk.Toplevel(self.root)
#         top.title(title)
#         top.iconphoto(False, photo)
        
#         # Main frame
#         frame = tk.Frame(top)
#         frame.pack(padx=(20, 0), pady=(10, 5), fill=tk.BOTH, expand=True)
        
#         # Inner frame for icon and text
#         inner_frame = tk.Frame(frame)
#         inner_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Icon
#         icon_label = tk.Label(inner_frame, image=photo)
#         icon_label.image = photo
#         icon_label.pack(side=tk.LEFT, padx=10)
        
#         # Calculate optimal text dimensions
#         max_width = min(600, self.root.winfo_screenwidth() - 100)  # Maximum width with screen consideration
#         text_width, text_height = self.calculate_text_dimensions(message, max_width)
        
#         # Text widget
#         label = tk.Text(inner_frame, wrap=tk.WORD, font=self.font, bg=top.cget('bg'), bd=0)
#         label.insert(tk.END, message)
#         label.config(
#             state=tk.DISABLED,  # Make it read-only
#             width=text_width // self.font.measure('0'),  # Convert pixels to character width
#             height=text_height // self.font.metrics('linespace')  # Convert pixels to line height
#         )
#         label.pack(padx=10, pady=(20, 10), fill=tk.BOTH, expand=True)
        
#         # OK button
#         button = ttk.Button(frame, text="OK", command=top.destroy)
#         button.pack(pady=10, side=tk.BOTTOM)
        
#         # Window positioning and sizing
#         top.update_idletasks()
        
#         # Calculate final window dimensions
#         window_width = min(text_width + 150, max_width)  # Add padding for icon and margins
#         window_height = text_height + 100  # Add space for button and margins
        
#         # Center window on screen
#         screen_width = top.winfo_screenwidth()
#         screen_height = top.winfo_screenheight()
#         x = (screen_width - window_width) // 2
#         y = (screen_height - window_height) // 2
        
#         # Set window geometry
#         top.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
#         top.resizable(False, False)  # Disable window resizing
