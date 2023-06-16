import shutil
from collections import Counter
import webbrowser

def create_gui_window(coins, total):
    # Copy the template HTML file
    shutil.copyfile('result_template.html', 'output.html')

    # Read the copied HTML file
    with open('output.html', 'r') as file:
        html_content = file.read()

    # Replace the placeholders with the provided values
    html_content = html_content.replace('original_img', "/tmp/original.png")
    html_content = html_content.replace('labeled_img', "/tmp/labeled.png")
    html_content = html_content.replace('rect_img', "/tmp/rect.png")
    html_content = html_content.replace('detected_coins_img', "/tmp/detected_coins.png")

    for key, value in count_values(coins).items():
        if key == "1ct":
            html_content = html_content.replace('one_cent_amount', value)
        if key == "2ct":
            html_content = html_content.replace('two_cent_amount', value)
        if key == "5ct":
            html_content = html_content.replace('five_cent_amount', value)
        if key == "10ct":
            html_content = html_content.replace('ten_cent_amount', value)
        if key == "20ct":
            html_content = html_content.replace('twenty_cent_amount', value)
        if key == "50ct":
            html_content = html_content.replace('fifty_cent_amount', value)
        if key == "1€":
            html_content = html_content.replace('one_euro_amount', value)     
        if key == "2€":
            html_content = html_content.replace('two_euro_amount', value)

    html_content = html_content.replace('total_amount', "{:.2f}".format(total))

    # Write the modified HTML content to the output file
    with open('output.html', 'w') as file:
        file.write(html_content)

    # Open the temporary HTML file in a web browser
    webbrowser.open('output.html')

def count_values(lst):
    # Use Counter to count the occurrences of values in the list
    value_counts = Counter(lst)

    # Create a list of [value, count] lists
    value_count_list = [[value, count] for value, count in value_counts.items()]

    return value_count_list
    