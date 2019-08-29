# -*- coding=utf-8 -*-

from PIL import Image
import argparse

# Add command arguments
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-o', '--output')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)

# Get arguments
args = parser.parse_args()

IMG = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

# Define the ascii characters used to replace the colors
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# Map the 256 grey scale to the 70 characters above
def get_char(r, g, b, alpha=256):
	if alpha == 0:
		return ' '

	gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

	# Hash the color to the characters
	return ascii_char[gray % len(ascii_char)]


if __name__ == '__main__':
	im = Image.open(IMG)
	im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

	txt = ""

	for i in range(HEIGHT):
		for j in range(WIDTH):
			txt += get_char(*im.getpixel((j, i)))
		txt += '\n'

	print(txt)

	if OUTPUT:
		with open(OUTPUT,'w') as f:
			f.write(txt)
	else:
		with open('output.txt', 'w') as f:
			f.write(txt)
