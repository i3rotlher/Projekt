from skimage import io
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import image_preprocessing as ip

def segment_coins(image):
    segmented_coins = sequential_labeling(image)
    return segmented_coins

def sequential_labeling(image):
    H, W = image.shape
    
    # Pass 1 - Assign Initial Labels
    m = 2
    collisions = set()  # Set to hold label collisions
    
    for v in range(H):
        for u in range(W):
            if image[v][u] == 1:
                neighbors = get_neighbors(image, v, u)
                
                if all(n == 0 for n in neighbors):
                    image[v][u] = m
                    m = m + 1
                elif sum(n > 1 for n in neighbors) == 1:
                    neighbor_label = next(n for n in neighbors if n > 1)
                    image[v][u] = neighbor_label
                elif sum(n > 1 for n in neighbors) > 1:
                    neighbor_labels = [n for n in neighbors if n > 1]
                    selected_label = neighbor_labels[0]
                    image[v][u] = selected_label
                    for neighbor_label in neighbor_labels:
                        if neighbor_label != selected_label:
                            collisions.add((neighbor_label, selected_label))
                else:
                    image[v][u] = m
                    m += 1
        
    # Pass 2 - Resolve Label Collisions
    labels = list(range(2, m))
    sets = [{label} for label in labels]
    
    for collision in collisions:
        a, b = collision
        set_a = next(s for s in sets if a in s)
        set_b = next(s for s in sets if b in s)
        
        if set_a != set_b:
            set_a.update(set_b)
            sets.remove(set_b)
    
    # Pass 3 - Relabel the Image
    for v in range(H):
        for u in range(W):
            label = image[v][u]
            if label > 1:
                label_set = next(s for s in sets if label in s)
                representative = min(label_set)
                image[v][u] = representative
    
    return image

def get_neighbors(image, v, u):
    H, W = image.shape
    neighbors = []
    
    for dv in range(-1, 2):
        for du in range(-1, 2):
            if dv == 0 and du == 0:
                continue
            
            nv = v + dv
            nu = u + du
            
            if 0 <= nv < H and 0 <= nu < W:
                neighbors.append(image[nv][nu])
                
    return neighbors

def calculateCircleWidth(img):
    """
    This function calculates rectangles around each circle labled in the image.

    Args:
        img (np-array): labled img
        
    Returns:
        The rectangles in an array aroung each circle found. 
    """
    # dict: key = lable:[links, rechts]
    label_min_max = {}
    lines_y_coordinate = {}
    H, W = img.shape
    for y in range(H):
        for x in range(W):
            label = img[y,x]
            if label > 0:
                if label not in label_min_max:
                    label_min_max[label] = [x, x]
                else:
                    indices = np.where(img[y] == label)
                    # save most left coordainte
                    if indices[0][0] <= label_min_max[label][0] and indices[0][-1] >= label_min_max[label][1]:
                        # y axis is the same for min and max
                        label_min_max[label] = [indices[0][0], indices[0][-1]]
                        lines_y_coordinate[label] = y

    widths = {}
    lines = {}
    for key, value in label_min_max.items():
        # set x for min coordinate and max coordinate
        lines[key] = [value[0],value[1],lines_y_coordinate[key]]
        # calculate width
        widths[key] = (value[1]-value[0])/2

    return widths, lines

def getRectangleCoordinates(img):
    # x min, x max, y min, y max
    label_rectangles = {}
    H, W = img.shape
    for y in range(H):
        for x in range(W):
            label = img[y,x]
            if label > 0:
                if label not in label_rectangles:
                    label_rectangles[label] = [x, y, x, y]
                else:
                    if x < (label_rectangles[label][0]):
                        label_rectangles[label][0] = x
                    if y < (label_rectangles[label][1]):
                        label_rectangles[label][1] = y
                    if x > (label_rectangles[label][2]):
                        label_rectangles[label][2] = x
                    if y > (label_rectangles[label][3]):
                        label_rectangles[label][3] = y

    return label_rectangles

def get_circle_in_rectangles(img, rectangles):
    circles = []
    for lable, rectangle in rectangles.items():
        x_min, y_min, x_max, y_max = rectangle
        pixels =  np.zeros((y_max-y_min+1,x_max-x_min+1,3), dtype=np.uint8)

        radius = min(x_max - x_min, y_max - y_min) // 2

        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2

        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if (i - center_x)**2 + (j - center_y)**2 <= radius**2:
                    pixels[j-y_min,i-x_min]=img[j, i]
        
        circles.append(pixels)

    return circles
