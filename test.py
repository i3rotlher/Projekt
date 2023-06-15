from skimage import io
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import image_preprocessing as ip

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

    plt.subplot(221)
    plt.imshow(image, cmap='gray')
    plt.title("Original Image 1")
    plt.axis('off')
    plt.show()
        
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


binary_image1 = ip.to1Bit(ip.preprocess_image(io.imread("image.png")), 50)


plt.subplot(221)
plt.imshow(binary_image1, cmap='gray')
plt.title("Original Image 1")
plt.axis('off')
plt.show()

labeled_image1 = sequential_labeling(binary_image1)

plt.subplot(221)
plt.imshow(io.imread("image.png"), cmap='gray')
plt.title("Original Image 1")
plt.axis('off')

plt.subplot(222)
plt.imshow(labeled_image1, cmap='jet')
plt.title("Labeled Image 1")
plt.axis('off')

plt.show()