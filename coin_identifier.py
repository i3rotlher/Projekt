import coin_segmantation as cs
import numpy as np
import math

coin_widths = {"2€": 129, "1€": 113, "50ct": 118, "20ct": 103, "10ct":95, "5ct": 97, "2ct": 90, "1ct": 80}
coin_colors = {"ct":[171.69511425,94.07738922,18.88473678], "0ct": [147.46649621,128.30391465,13.07608887], "1€": [107.71024465,117.92830445,37.73292559], "2€": [147.0639613,147.41447192,58.01666219]}

def identifyCoins(image, coin_rectangles):
    coins = []

    for key, coin_rec in coin_rectangles.items():
        coin_cutout = cs.get_circle_in_rectangles(image, {key: coin_rec})[0]
        coins.append(identifyCoin(coin_rec, coin_cutout))
    
    return coins

def identifyCoin(coin_rec, coin_cutout):
    x_min, y_min, x_max, y_max = coin_rec
    width = x_max - x_min

    width_guess,second_width_guess = analyzeWidth(width)
    color_guess = analyzeColor(coin_cutout)

    if width_guess == color_guess:
        return width_guess

    if width_guess in color_guess:
        return width_guess
    
    if second_width_guess in color_guess:
        return second_width_guess
    
    return "No Clue ? widthguess = " + str(width_guess) + "," + str(second_width_guess) + "; color_guess = " + str(color_guess)

def analyzeWidth(width):
    return find_closest_width(width)

def find_closest_width(number):
    differences = {}
    
    for key, value in coin_widths.items():
        diff = abs(number - value)
        differences[key] = diff
    
    sorted_diff = sorted(differences.items(), key=lambda x: x[1])
    
    closest_key = sorted_diff[0][0]
    second_closest_key = sorted_diff[1][0]
    
    return closest_key, second_closest_key

def analyzeColor(coin_cutout):
    # average_color = np.mean(coin_cutout, axis=(0, 1))
    # return find_closest_color(average_color)

    # check euros
    # silver = silverAmount(coin_cutout)

    # if "€" in silver:      
    #     return ["1€", "2€"]
    
    red = calculate_average_red(coin_cutout)
    blue = calculate_average_blue(coin_cutout)
    green = calculate_average_green(coin_cutout)

    if abs(red-green) < 30 and blue > 40:
        return ["1€", "2€"]

    if red-green < 35:
        return ["10ct", "20ct", "50ct"]

    return ["1ct", "2ct", "5ct"]

# not used
def find_closest_color(color):
    closest_color_value = None
    closest_color_distance = float('inf')

    for dict_color, dict_value in coin_colors.items():
        distance = calculate_color_distance(color, dict_value)
        if distance < closest_color_distance:
            closest_color_distance = distance
            closest_color_value = dict_color

    return closest_color_value

def calculate_color_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    distance = math.sqrt((r2 - r1)**2 + (g2 - g1)**2 + (b2 - b1)**2)
    return distance

def silverAmount(coin_cutout):
    amount = np.sum(coin_cutout > [150, 150, 150])
    if amount > 25000:
        return "2€"
    if amount > 20000 and amount < 25000:
        return "1€"
    else:
        return "ct" 
    
# in use
def calculate_average_red(image):
    red_channel = image[:,:,0]  # Extract the red channel
    non_black_pixels = red_channel > 0  # Create a mask for non-black pixels
    red_values = red_channel[non_black_pixels]  # Filter the red values using the mask
    average_red = np.mean(red_values)  # Calculate the average red value
    return average_red

def calculate_average_blue(image):
    red_channel = image[:,:,2]  # Extract the red channel
    non_black_pixels = red_channel > 0  # Create a mask for non-black pixels
    red_values = red_channel[non_black_pixels]  # Filter the red values using the mask
    average_red = np.mean(red_values)  # Calculate the average red value
    return average_red

def calculate_average_green(image):
    red_channel = image[:,:,1]  # Extract the red channel
    non_black_pixels = red_channel > 0  # Create a mask for non-black pixels
    red_values = red_channel[non_black_pixels]  # Filter the red values using the mask
    average_red = np.mean(red_values)  # Calculate the average red value
    return average_red
