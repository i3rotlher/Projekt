from skimage import io, color
import numpy as np

def read_image(image_path):
    image = io.imread(image_path)
    return image