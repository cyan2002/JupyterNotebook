#This will read images and show them

# Imports PIL module
from PIL import Image

# open method used to open different extension image file
im = Image.open(r"/Users/chanceyan/Documents/Python/Images/Ysabella.jpeg")

# This method will show image in any image viewer
im.show()