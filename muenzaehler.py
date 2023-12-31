import coin_segmantation as cs
import coin_identifier as ci
import image_preprocessing as ip
import imager_reader as ir
import matplotlib.pyplot as plt
import glob
import GUI.gui as gui

def map_coin_to_float(coin):
    if coin == '1ct':
        return 0.01
    elif coin == '2ct':
        return 0.02
    elif coin == '5ct':
        return 0.05
    elif coin == '10ct':
        return 0.10
    elif coin == '20ct':
        return 0.20
    elif coin == '50ct':
        return 0.50
    elif coin == '1€':
        return 1.00
    elif coin == '2€':
        return 2.00
    else:
        return None

def countCoins(coins):
    total = 0.0
    coins_counts = {}
    for coin in coins: 
        total += map_coin_to_float(coin)
        if coin in coins_counts:
            coins_counts[coin] = coins_counts[coin] + 1
        else:
            coins_counts[coin] = 1
    return total, coins_counts
    
def plot_images(images, titles, num_cols=3):
    num_cols = min(3, len(images))
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

    # Remove empty subplots if necessary
    if num_images < num_rows * num_cols:
        for j in range(num_images, num_rows * num_cols):
            if num_rows > 1:
                ax = axes[j // num_cols, j % num_cols]
            else:
                ax = axes[j % num_cols]
            ax.axis('off')
            ax.set_visible(False)

    plt.savefig("GUI/tmp/detected_coins.png")
    plt.close()

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

def muenzenZaehlen(imgpath): 
    original = ir.read_image(imgpath)
    binary_image = ip.to1Bit(ip.preprocess_image(original), 50)
    labeled_image = cs.segment_coins(binary_image)
    rectangles = cs.getRectangleCoordinates(labeled_image)
    image_rects = drawRectangles(original, rectangles)

    # Figure 1
    plt.figure()
    plt.imshow(original)
    plt.axis('off')
    plt.savefig("GUI/tmp/original.png")

    # Figure 2
    plt.figure()
    plt.imshow(labeled_image, cmap='jet')
    plt.axis('off')
    plt.savefig("GUI/tmp/labeled.png")

    # Figure 3
    plt.figure()
    plt.imshow(image_rects, cmap="jet")
    plt.axis('off')
    plt.savefig("GUI/tmp/rect.png")

    coins_found = ci.identifyCoins(original, rectangles)
    plot_images(cs.get_circle_in_rectangles(original, rectangles), coins_found)
    total, coin_counts = countCoins(coins_found)

    plt.close('all')
    gui.create_gui_window(coin_counts, total)

def main():
    png_files = []

    for file_path in glob.glob('inputs/*.png'):
        png_files.append(file_path)

    for file in png_files:
        muenzenZaehlen(file)

main()