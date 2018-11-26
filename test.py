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
original = loadImage("parrot.jpeg")
#colors = getHSLColors(4, 1, 2)
#colors = getHSLColors(7, 1, 2) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
#colors = getHSLColors(3, 1, 1) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
colors = getMostCommonColors(original, 8)
randomDither(original, colors, 15).save("outputr.png")
threshold(original, colors).save("outputt.png")
dither2x2(original, colors, 1/4, 1/8).save("output2x2.png")
dither2x2(original, colors, 1/3, 1/5).save("output2x2t.png")
dither3x3(original, colors, 1/5, 1/10).save("output3x3.png")
