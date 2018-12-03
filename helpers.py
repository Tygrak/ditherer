from PIL import Image
import math
import random
import colorsys
import numpy

def getDistance(color1, color2):
    return math.sqrt((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)

def manhattanDistance(color1, color2):
    return abs(color1[0]-color2[0])+abs(color1[1]-color2[1])+abs(color1[2]-color2[2])

def averagePixelColors(toAverage):
    average = [0, 0, 0]
    for pixel in toAverage:
        average[0] += pixel[0]
        average[1] += pixel[1]
        average[2] += pixel[2] 
    average[0] //= len(toAverage)
    average[1] //= len(toAverage)
    average[2] //= len(toAverage)
    return tuple(average)

def loadImage(path):
    try:
        original = Image.open(path)
    except:
        print("Unable to load image")
    original = original.convert("RGB")
    return original
