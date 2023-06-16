import shutil
from collections import Counter
import webbrowser

def create_gui_window(coins, total):
    # Copy the template HTML file
    shutil.copyfile('GUI/result_template.html', 'GUI/tmp/output.html')

    # Read the copied HTML file
    with open('GUI/tmp/output.html', 'r') as file:
        html_content = file.read()

    # Replace the placeholders with the provided values
    html_content = html_content.replace('original_img', "C:/Users/skill/OneDrive/AIN/Semester 8/2D-ComputerVision/Projekt/GUI/tmp/original.png")
    html_content = html_content.replace('labled_img', "C:/Users/skill/OneDrive/AIN/Semester 8/2D-ComputerVision/Projekt/GUI/tmp/labeled.png")
    html_content = html_content.replace('rect_img', "C:/Users/skill/OneDrive/AIN/Semester 8/2D-ComputerVision/Projekt/GUI/tmp/rect.png")
    html_content = html_content.replace('detected_coins_img', "C:/Users/skill/OneDrive/AIN/Semester 8/2D-ComputerVision/Projekt/GUI/tmp/detected_coins.png")


    html_content = html_content.replace('one_cent_amount', str(coins["1ct"] or 0))
    html_content = html_content.replace('two_cent_amount', str(coins["2ct"] or 0))
    html_content = html_content.replace('five_cent_amount', str(coins["5ct"] or 0))
    html_content = html_content.replace('ten_cent_amount', str(coins["10ct"] or 0))
    html_content = html_content.replace('twenty_cent_amount', str(coins["20ct"] or 0))
    html_content = html_content.replace('fifty_cent_amount', str(coins["50ct"] or 0))
    html_content = html_content.replace('one_euro_amount', str(coins["1€"] or 0))     
    html_content = html_content.replace('two_euro_amount', str(coins["2€"] or 0))

    html_content = html_content.replace('total_amount', "{:.2f}".format(total))

    # Write the modified HTML content to the output file
    with open('GUI/tmp/output.html', 'w') as file:
        file.write(html_content)

    import webbrowser

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'  # Replace with the actual Chrome executable path
    html_file_path = 'C:/Users/skill/OneDrive/AIN/Semester 8/2D-ComputerVision/Projekt/GUI/tmp/output.html'  # Replace with the actual HTML file path

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(html_file_path)

def count_coins(coins):
    # Use Counter to count the occurrences of values in the list
    value_counts = {}

    for coin in coins:
        if coin in value_counts:
            value_counts[coin] = value_counts[coin] + 1
        else:
            value_counts[coin] = 1

    return value_counts
    