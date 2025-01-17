import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import imageio
import sys
from PIL import Image

# Load the image
# image_path = r"C:\Users\NDT Lab\Software\tinkterApp\clearCpu.png"  # Replace with your image file path
# image_path = r"C:\Users\NDT Lab\Software\tinkterApp\what-is-noise-in-photography-title-2460x1440.jpg"  # Replace with your image file path
image_path = r"C:\Users\NDT Lab\Software\tinkterApp\sample-test.png"  # Replace with your image file path

image = plt.imread(image_path)


if image.ndim == 3:  # Check if the image has color channels
    image = np.mean(image, axis=2)  # Convert to grayscale by averaging the color channels


# dx = ndimage.sobel(image, 0)  # horizontal derivative
# dy = ndimage.sobel(image, 1)  # vertical derivative
# mag = np.hypot(dx, dy)  # magnitude
# mag *= 255.0 / np.max(mag)  # normalize (Q&D)
# mag = mag.astype(np.uint8)
# # imageio.imwrite("sobel with imageio.jpg", mag)
# plt.title("scipy Sobel filter")
# plt.imshow(mag)
# plt.show()

# sys.exit(0)

# Convert to grayscale if the image is in color
# if len(image.shape) == 3:
#     gray_image = np.mean(image, axis=2)  # Simple average for grayscale
# else:
#     gray_image = image

gray_image = image
# Define Sobel kernels
sobel_x = np.array([[1, 0, -1],
                    [2, 0, -2],
                    [1, 0, -1]])

sobel_y = np.array([[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]])

# Apply Sobel filter using convolution
sobel_x_result = ndimage.convolve(gray_image, sobel_x)
sobel_y_result = ndimage.convolve(gray_image, weights=sobel_y)

# Calculate the magnitude of the gradient
sobel_magnitude = np.sqrt(sobel_x_result**2 + sobel_y_result**2)

# Normalize the result to the range [0, 255]
sobel_magnitude = np.clip(sobel_magnitude, 0, 255).astype(np.uint8)

# Display the results
plt.figure(figsize=(10, 5))
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Sobel X')
plt.imshow(sobel_x_result, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Sobel Y')
plt.imshow(sobel_y_result, cmap='gray')
plt.axis('off')

plt.figure(figsize=(5, 5))
plt.title('Sobel Magnitude')
plt.imshow(sobel_magnitude, cmap='gray')
plt.axis('off')

plt.show()
