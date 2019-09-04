from PIL import Image
import time
import os
import math
import hashlib


class VectorCompare(object):
    # Compute the magnitude of the vector. Used for vector normalisation
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance:
            total += count ** 2
        return math.sqrt(total)

    # Compute the cosine similarity of two vectors
    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

# Flat the image to vector
def buildvector(im):
    d1 = {i: pix for i, pix in enumerate(im.getdata())}
    return d1

v = VectorCompare()

iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h',
           'i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Load training data
imageset = []
for letter in iconset:
    for img in os.listdir('/iconset/%s/'%(letter)):
        temp = []
        temp.append(buildvector(Image.open('/iconset/%s/%s'%(letter, img))))
        imageset.append({letter: temp})

# Convert the original image to binary image
im = Image.open('data/captcha.gif')
im.convert('P')  # convert to 8 bit pixels
im2 = Image.new('P', im.size, 255)
for x in range(im.size[0]):
    for y in range(im.size[1]):
        pix = im.getpixel([x, y])
        if pix == 220 or pix == 227:  # these are the red pixel
            im2.putpixel([x, y], 0)

# Slice the image vertically to get single character in the image
# Get the start and end column value for each character
start, end = 0, 0  # initialise the start and end column for the characters
inletter, foundletter = False, False
letters = []
for x in range(im2.size[0]):
    for y in range(im2.size[1]):  # iter different in height value
        pix = im2.getpixel([x, y])
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = x
    if foundletter == True and inletter == False:
        foundletter = False
        end = x
        letters.append([start, end])
    inletter = False

# Get the slice with letter
count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    guess = []

    for img in imageset:
        for letter, y in img.iteritem():
            if len(y) != 0:
                guess.append((v.relation(buildvector(im3), y[0]), x))
    guess.sort(reverse=True)
    print('', guess[0])
    count += 1
