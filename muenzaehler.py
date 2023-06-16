import coin_segmantation as cs
import coin_identifier as ci
import image_preprocessing as ip
import imager_reader as ir
import matplotlib.pyplot as plt
import numpy as np

def muenzenZaehlen(): 
    original = ir.read_image("image.png")
    binary_image = ip.to1Bit(ip.preprocess_image(original), 50)
    labeled_image = cs.segment_coins(binary_image)

    # widths, lines = cs.calculateCircleWidth(labeled_image)
    # image_widths = original.copy()
    # image_widths = labeled_image.copy()
    # for line in lines.values():
    #     for x in range(line[0],line[1]+1):
    #         image_widths[line[2], x] = 69

    rectangles = cs.getRectangleCoordinates(labeled_image)
    image_rects = drawRectangles(original, rectangles)

    plt.subplot(221)
    plt.imshow(original)
    plt.title("Original Image 1")
    plt.axis('off')

    plt.subplot(222)
    plt.imshow(labeled_image, cmap='jet')
    plt.title("Labled Image 1")
    plt.axis('off')

    plt.subplot(223)
    plt.imshow(image_rects, cmap="jet")
    plt.title("Image with rectangles")
    plt.axis('off')
    plt.show()

    coins_found = ci.identifyCoins(original, rectangles)
    plot_images(cs.get_circle_in_rectangles(original, rectangles), coins_found)

def plot_images(images, titles, num_cols=3):
    num_images = len(images)
    num_rows = (num_images + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 10))
    fig.tight_layout()

    for i, image in enumerate(images):
        if num_rows > 1:
            ax = axes[i // num_cols, i % num_cols]
        else:
            ax = axes[i % num_cols]
        ax.imshow(image)
        ax.set_title(titles[i])
        ax.axis('off')

    plt.show()

def drawRectangles(img, rectanglesCoordinates): 
    new_img = img.copy()
    for rectangle in rectanglesCoordinates.values():
        x_min, y_min, x_max, y_max = rectangle
        for y in [y_min, y_max+1]:
            for x in range(x_min, x_max+1):
                new_img[y,x] = [255,0,0]
        for x in [x_min, x_max+1]:
            for y in range(y_min, y_max+1):
                new_img[y,x] = [255,0,0]
    return new_img

if __name__ == "__main__":
    muenzenZaehlen()

muenzenZaehlen()
