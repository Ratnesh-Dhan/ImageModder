import sys



def circular():
    pass
    
    

if __name__ == '__main__':
    ary = [0,1,1,0,0]
    #l=0
    l=0
    f=1
    #ary[:] = [None] * len(ary)
    input1 = ''
    while input1 != -1:
        print(f"first :{f}, last :{l}")
        input1 = int(input(f"enter a value: {ary} "))
        #if len(ary) < 5:
            #l = l+1
           # ary.append(input1)
           
        #elif len(ary) == 5:
        
        if f-l == -4 or f-l ==1:
            if l == 4:       
                f = f+1
                l = 0
                ary[l] = input1
            elif f == 4:
                
                f = 0
                l = l+1
                ary[l] = input1
            else:
                
                l = 1+l
                f = 1+f
                ary[l] = input1
        else:
            l = (l+1)%5
            ary[l] = input1


sys.exit(1)
from PIL import Image
import matplotlib.pyplot as plt

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        if image:
            print(image)
    except Exception as e:
        print(f"Something went wrong {e}")

#print(extract_text_from_image('src/public/icon.png'))

def RGB_channels():
    img = plt.imread("./src/public/color.jpg")
    #s = plt.imshow(img)
    
    plt.subplot(1, 3, 1)
    plt.imshow(img[:,:, 0], cmap=None)
    plt.title("red channel")
    
    plt.subplot(1,3,2)
    plt.imshow(img[:, :, 1], cmap=None)
    plt.title("green channel")
    
    plt.subplot(1,3,3)
    plt.imshow(img[:, :, 1], cmap=None)
    plt.title("blue channel")
    
    #plt.hist(img.flatten())
    plt.show()
 
def backup():
    import tkinter as tk
    
    root = tk.Tk()
    root.title("test menu")
    #Creating menubar
    menubar = tk.Menu(root)
    
    #Adding a menu and command
    test = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="file", menu=test)
    test.add_command(label="New File", command=lambda: print("New File"))
    
    root.config(menu = menubar)
    tk.mainloop()
