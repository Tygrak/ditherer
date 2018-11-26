from PIL import Image
import math
import random
import colorsys
import numpy

from helpers import *

def getGreyscaleColors(amount):
    colors = []
    for i in range(amount):
        shade = (255*i)//(amount-1)
        colors.append((shade, shade, shade))
    return colors

def getHSLColors(huesNum, saturationsNum, lightnessNum):
    colors = []
    for i in range(huesNum):
        for j in range(1, saturationsNum+1):
            for k in range(lightnessNum):
                lightness = 0.5 if lightnessNum == 1 else (0.2+0.6*k)/lightnessNum
                r, g, b = colorsys.hls_to_rgb(i/huesNum, lightness, j/saturationsNum)
                colors.append((round(r*255), round(g*255), round(b*255)))
    return colors

def getMostCommonColors(image, amount):
    resized = image.resize((amount, amount), Image.ANTIALIAS)
    pixels = list(resized.getdata())
    counts = [0 for i in range(len(pixels))] 
    fuzz = 50
    for i in range(len(pixels)):
        for j in range(len(pixels)):
            if getDistance(pixels[i], pixels[j]) < fuzz:
                counts[i] += 1
    counts = [(i, counts[i]) for i in range(len(counts))]
    sortedCounts = sorted(counts, key = lambda x: x[1], reverse = True)
    fuzz2 = 150
    for i in range(len(sortedCounts)):
        for j in range(i):
            if getDistance(pixels[sortedCounts[i][0]], pixels[sortedCounts[j][0]]) < fuzz2:
                sortedCounts.append(sortedCounts.pop(i))
                break
    colors = [pixels[x[0]] for x in sortedCounts[:amount]]
    print(colors)
    return colors