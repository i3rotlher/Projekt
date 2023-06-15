import coin_segmantation as cs
import image_preprocessing as ip
import imager_reader as ir
import matplotlib.pyplot as plt


def muenzenZaehlen(): 
    binary_image = ip.to1Bit(ip.preprocess_image(ir.read_image("image.png")), 50)
    labeled_image = cs.segment_coins(binary_image)

    widths, lines = cs.calculateCircleWidth(labeled_image)
    # image_widths = ir.read_image("image.png").copy()
    # image_widths = labeled_image.copy()
    # for line in lines.values():
    #     for x in range(line[0],line[1]+1):
    #         image_widths[line[2], x] = 69

    image_rects = cs.drawRectangles(ir.read_image("image.png"), cs.getRectangleCoordinates(labeled_image))

    print(widths)

    plt.subplot(221)
    plt.imshow(ir.read_image("image.png"))
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

if __name__ == "__main__":
    muenzenZaehlen()

muenzenZaehlen()