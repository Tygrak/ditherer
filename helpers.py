from PIL import Image
import math
import random
import colorsys
import numpy

def getDistance(color1, color2):
    return math.sqrt((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)

def loadImage(path):
    try:
        original = Image.open(path)
    except:
        print("Unable to load image")
    original = original.convert("RGB")
    return original
