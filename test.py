from PIL import Image
import math
import random
import colorsys
import numpy

from ditherers import *
from colors import *
from helpers import *

#original = loadImage("gradient.png")
#original = loadImage("parrot.jpg")
#original = loadImage("coolpic.jpeg")
#original = loadImage("desert.jpg")
original = loadImage("milk.jpg")
#colors = getHSLColors(4, 1, 2)
#colors = getHSLColors(7, 1, 2) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
#colors = getHSLColors(3, 1, 1) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
#colors = getImagePaletteRandAlg(original, 8)
#print(colors)
colors = getImagePaletteMedianCut(original, 16)
print(colors)
colors = saturateColors(colors, 1.5)
colors = lightenColors(colors, 1.1)
#print(colors)
#pixels = dither2x2(original, colors, 1/4, 1/8)
#imageCopyPixels(original, dither2x2(original, colors, 1/4, 1/8)).save("output/outputpixels.png")
#pixels = shiftHueColors(pixels, 0.75)
#imageCopyPixels(original, pixels).save("output/changedpixels.png")

imageCopyPixels(original, randomDither(original, colors, 10)).save("outputShowcase/outputr.png")
imageCopyPixels(original, threshold(original, colors)).save("outputShowcase/outputt.png")
imageCopyPixels(original, dither2x2(original, colors, 1/4, 1/8)).save("outputShowcase/output2x2.png")
imageCopyPixels(original, dither2x2(original, colors, 1/3, 1/5)).save("outputShowcase/output2x2b.png")
imageCopyPixels(original, dither3x3(original, colors, 1/5, 1/10)).save("outputShowcase/output3x3.png")
