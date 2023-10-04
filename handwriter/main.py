from PIL import Image, ImageDraw, ImageFont
import json
import random

char_list_add = ['.', ',', ':', ';', '-', '(', ')', '*']
font_main_list = []

with open('config_main.json', 'r') as f:
    config_main = json.load(f)
    height = config_main.get('height', 0)
    width = config_main.get('width', 0)
    height_spacings = config_main.get('height_spacings', 0)
    x_zero_offset = config_main.get('x_zero_offset', 0)
    y_zero_offset = config_main.get('y_zero_offset', 0)
    y_char_to_line_offset = config_main.get('y_char_to_line_offset', 0)
    font_spacing = config_main.get('font_spacing', 0)
    font_size = config_main.get('font_size', 0)
    rondom_font = config_main.get('rondom_font', "False")
    line_color_bool = config_main.get('line', "False")
    # define the default spacing before and after each character
    default_space_before = 0
    default_space_after = 0

if line_color_bool == "True":
    line_color = (0, 0, 0)  # цвет линий
else:
    line_color = (255, 255, 255)

# define the font
font_path = 'handfont-rus.ttf'
font_main = ImageFont.truetype(font_path, font_size)
font_main_list.append(font_main)

font_path_add = 'handfont-rus-add.ttf'
font_add = ImageFont.truetype(font_path_add, font_size)

if rondom_font == "True":
    font_path2 = 'handfont-rus2.ttf'
    font_main2 = ImageFont.truetype(font_path, font_size)
    font_main_list.append(font_main2)

with open('config_font.json', 'r') as f:
    config_font = json.load(f)

with open('text.txt', 'r') as f:
    text = f.read()

# create the ImageDraw object
image = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

x = x_zero_offset
y = y_zero_offset + y_char_to_line_offset

# render each character
while y < height:
    draw.line((0, y, width, y), fill=line_color, width=1)
    y += height_spacings

y = y_zero_offset

# split the text into words
text = text.replace("\n", " | ")
text = text.replace("\t", " ` ")
words = text.split()

# render each word
for word in words:
    x += random.randrange(30, 50)
    if(len(word) * 30) > (width - x):
        y = y + height_spacings
        x = x_zero_offset + random.randrange(0, 20)
    elif word == '`':    # проверяем на \t
        x += 90
        continue
    elif word == '|':     # проверяем на \n
        y = y + height_spacings
        x = x_zero_offset + random.randrange(0, 20)
        continue

    for char in word:
        # get the spacing before and after the current character from the config file(json)
        char_spacing = config_font.get(char, {}).get('spacing', 0)
        char_space_before = config_font.get(char, {}).get('space_before', 0)

        if char in char_list_add:   # выбор шрифта
            font = font_add
        elif 'А' <= char <= 'я' or '0' <= char <= '9':
            font = random.choice(font_main_list)
        else:
            continue

        # get the bounding box of the character
        char_bbox = draw.textbbox((x + char_space_before, 10), char, font=font)
        char_width = char_bbox[2] - char_bbox[0]
        char_height = char_bbox[3] - char_bbox[1]

        # render the character
        draw.text((x + char_space_before + random.randrange(-1, 1), y + random.randrange(-3, 3)), char, font=font,fill=(0, 0, 0))

        # update the x coordinate for the next character
        x += char_width + char_spacing + char_space_before + font_spacing

# save the image
image.save('output.png')
image.show()