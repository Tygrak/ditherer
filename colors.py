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

def lightenColors(colors, scalar):
    newColors = []
    for i in range(len(colors)):
        h, s, l = colorsys.rgb_to_hls(colors[i][0]/255, colors[i][1]/255, colors[i][2]/255)
        r, g, b = colorsys.hls_to_rgb(h, s, min(l*scalar, 1))
        newColors.append((round(r*255), round(g*255), round(b*255)))
    return newColors

def saturateColors(colors, scalar):
    newColors = []
    for i in range(len(colors)):
        h, s, l = colorsys.rgb_to_hls(colors[i][0]/255, colors[i][1]/255, colors[i][2]/255)
        r, g, b = colorsys.hls_to_rgb(h, min(s*scalar, 1), l)
        newColors.append((round(r*255), round(g*255), round(b*255)))
    return newColors

def shiftHueColors(colors, shiftAmount):
    newColors = []
    for i in range(len(colors)):
        h, s, l = colorsys.rgb_to_hls(colors[i][0]/255, colors[i][1]/255, colors[i][2]/255)
        r, g, b = colorsys.hls_to_rgb((h+shiftAmount)%1, s, l)
        newColors.append((round(r*255), round(g*255), round(b*255)))
    return newColors


def getImagePaletteRandAlg(image, amount):
    resized = image.resize((min(amount*16, image.width), min(amount*16, image.width)), Image.ANTIALIAS)
    pixels = list(resized.getdata())
    colors = []
    for i in range(amount):
        currentMax = 600
        distance = 0
        randPixel = random.randint(0, len(pixels)-1)
        while (distance < currentMax and len(colors) > 0):
            randPixel = random.randint(0, len(pixels)-1)
            for color in colors:
                distance += manhattanDistance(pixels[randPixel], color)
            distance = distance/len(colors)
            currentMax -= 1;
        colors.append(pixels[randPixel])
    return colors

def getImagePaletteMedianCut(image, amount):
    def splitSortColors (toSplit):
        minColors = [255, 255, 255]
        maxColors = [0, 0, 0]
        for pixel in toSplit:
            for i in range(3):
                if (pixel[i] > maxColors[i]):
                    maxColors[i] = pixel[i]
                if (pixel[i] < minColors[i]):
                    minColors[i] = pixel[i]
        maxRange = 0
        sortKey = 0
        for i in range(3):
            crange = maxColors[i]-minColors[i]
            if (crange > maxRange):
                maxRange = crange
                sortKey = i
        toSplit = sorted(toSplit, key=lambda x: x[sortKey])
        return [toSplit[len(toSplit)//2:], toSplit[:len(toSplit)//2]]
    
    parts = []
    pixels = list(image.getdata())
    parts.append(pixels)
    for i in range(int(math.log2(amount))):
        for j in range(len(parts)-1, -1, -1):
            splitted = splitSortColors(parts[j])
            parts.pop(j)
            parts.append(splitted[0])
            parts.append(splitted[1])
    colors = [averagePixelColors(x) for x in parts]
    return colors