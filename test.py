from PIL import Image
import math
import random
import colorsys
import numpy

from ditherers import *
from colors import *
from helpers import *

#original = loadImage("gradient.png")
#original = loadImage("cat.jpeg")
original = loadImage("coolpic.jpeg")
#colors = getHSLColors(4, 1, 2)
#colors = getHSLColors(7, 1, 2) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
#colors = getHSLColors(3, 1, 1) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
#colors = getImagePaletteRandAlg(original, 4)
#print(colors)
#randomDither(original, colors, 15).save("outputrr.png")
#threshold(original, colors).save("outputrt.png")
#dither2x2(original, colors, 1/4, 1/8).save("outputr2x2.png")
colors = getImagePaletteMedianCut(original, 4)
print(colors)
colors = saturateColors(colors, 1.5)
colors = lightenColors(colors, 1.2)
colors = shiftHueColors(colors, 0.45)
print(colors)
randomDither(original, colors, 15).save("outputr.png")
threshold(original, colors).save("outputt.png")
dither2x2(original, colors, 1/4, 1/8).save("output2x2.png")
#dither2x2(original, colors, 1/3, 1/5).save("output2x2t.png")
#dither3x3(original, colors, 1/5, 1/10).save("output3x3.png")
