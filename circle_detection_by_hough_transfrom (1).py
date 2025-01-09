import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

# Load picture and detect edges
image = img_as_ubyte(data.coins()[160:230, 70:270])
edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)
plt.imshow(image,cmap='gray')

# Detect a range of radii
hough_radii = np.arange(20, 35, 2)
hough_res = hough_circle(edges, hough_radii)

# Visualize the Hough transform for one specific radius
fig, axes = plt.subplots(1, len(hough_radii), figsize=(15, 5), sharex=True, sharey=True)
for ax, radius, hough_slice in zip(axes, hough_radii, hough_res):
    ax.imshow(hough_slice, cmap="hot")
    ax.set_title(f"Hough Transform\nRadius: {radius}")
    ax.axis("off")

plt.tight_layout()
plt.show()

# Select the most prominent 3 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=3)

# Draw them
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
image = color.gray2rgb(image)
for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius, shape=image.shape)
    image[circy, circx] = (220, 20, 20)

ax.imshow(image, cmap=plt.cm.gray)
ax.set_title("Detected Circles")
plt.show()
