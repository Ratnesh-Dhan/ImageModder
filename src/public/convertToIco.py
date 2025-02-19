from PIL import Image
img = Image.open("research.png")
img.save("mainIcon.ico", format="ICO")