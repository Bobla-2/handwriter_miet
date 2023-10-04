import os
from PIL import Image, ImageDraw, ImageFont
import json
import random

char_list = ['.', ',', ':', ';', '-', '(', ')', '*']

height = 8000
width = 2560
height_spacings = 70

x_zero_offset = 100
y_zero_offset = 50
x_max_offset = 200

line_color = (0,0,0)

# define the font and size
font_path = 'handfont-rus.ttf'
font_size = 150
font_spacing = -20

# define the default spacing before and after each character
default_space_before = 0
default_space_after = 0

fallback_font = ImageFont.truetype('handfont-rus-add.ttf', size=font_size)

with open('config2.json', 'r') as f:
    config = json.load(f)

with open('text.txt', 'r') as f:
    text = f.read()

# create the PIL Image object
image = Image.new('RGB', (width, height), color = (255, 255, 255))

# create the ImageDraw object
draw = ImageDraw.Draw(image)

# create the font object
font = ImageFont.truetype(font_path, font_size)

# render the text
#draw.text((10, 10), text, font=font, fill=(0, 0, 0))


x = x_zero_offset
y = 72
# render each character
# render each character
while y < height:
    draw.line((0, y, width, y), fill=line_color, width=1 )
    y += height_spacings

y = y_zero_offset

# split the text into words
text = text.replace("\n", "|")
text = text.replace("\t", "`")

words = text.split()


# render each word
for word in words:
    if((len(word)*30) > (width - x)):
        y = y + height_spacings
        x = x_zero_offset + random.randrange(0, 20)
    if (width - x) < x_max_offset:
        y = y + height_spacings
        x = x_zero_offset + random.randrange(0, 20)
    for char in word:
        if char == '|':
            y = y + height_spacings
            x = x_zero_offset + random.randrange(0, 20)
        elif char == '`':
            x +=90
        else:
            # get the spacing before and after the current character from the config file
            char_config = config.get(char, {})
            char_spacing = char_config.get('spacing', default_space_after)
            char_space_before = char_config.get('space_before', default_space_before)

            font = ImageFont.truetype(font_path, font_size)
            #mask = (char)
            #mask = font.getmask(char)

            # if the mask is blank, use the fallback font instead
            if char in char_list:
                font = fallback_font
            # get the bounding box of the character
            char_bbox = draw.textbbox((x + char_space_before, 10), char, font=font)

            # calculate the width and height of the character
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]

            # render the character
            draw.text((x + char_space_before + + random.randrange(-1, 1), y+random.randrange(-3, 3)), char, font=font, fill=(0, 0, 0))

            # update the x coordinate for the next character
            x += char_width + char_spacing + char_space_before + font_spacing

            if x > (width):
                # render the character
                # draw.text((x + char_space_before + + random.randrange(-1, 1), y + random.randrange(-3, 3)), '-', font=font, fill=(0, 0, 0))

                x = x_zero_offset + random.randrange(0, 20)
                y = y + height_spacings
    x += random.randrange(30, 50)
# save the image
image.save('output.png')
image.show()