from PIL import Image
import math
import random
import colorsys
import numpy

from helpers import *

def threshold(image, colors):
    pixels = list(image.getdata())
    for i in range(len(pixels)):
        bestColorId = 0
        bestColorDistance = getDistance(pixels[i], colors[0])
        for j in range(1, len(colors)):
            dist = getDistance(pixels[i], colors[j])
            if dist < bestColorDistance:
                bestColorDistance = dist
                bestColorId = j
        pixels[i] = colors[bestColorId]
    return pixels

#errorR1 and R2 define the amount of error carried to surrounding squares
def dither2x2(image, colors, errorR1=1/4, errorR2=1/4):
    pixels = list(image.getdata())
    for i in range(len(pixels)):
        bestColorId = 0
        bestColorDistance = getDistance(pixels[i], colors[0])
        for j in range(1, len(colors)):
            dist = getDistance(pixels[i], colors[j])
            if dist < bestColorDistance:
                bestColorDistance = dist
                bestColorId = j
        error = numpy.subtract(pixels[i], colors[bestColorId])
        pixels[i] = colors[bestColorId]
        if i%image.width != image.width-1:
            pixels[i+1] = tuple(numpy.round(numpy.add(pixels[i+1], error*errorR1)).astype(int))
            if i+image.width+1 < len(pixels):
                pixels[i+image.width+1] = tuple(numpy.round(numpy.add(pixels[i+image.width+1], error*errorR2).astype(int)))
        if i+image.width < len(pixels):
            pixels[i+image.width] = tuple(numpy.round(numpy.add(pixels[i+image.width], error*errorR1).astype(int)))
    return pixels

def dither3x3(image, colors, errorR1 = 1/8, errorR2 = 1/16):
    pixels = list(image.getdata())
    for i in range(len(pixels)):
        bestColorId = 0
        bestColorDistance = getDistance(pixels[i], colors[0])
        for j in range(1, len(colors)):
            dist = getDistance(pixels[i], colors[j])
            if dist < bestColorDistance:
                bestColorDistance = dist
                bestColorId = j
        error = numpy.subtract(pixels[i], colors[bestColorId])
        pixels[i] = colors[bestColorId]
        # extremely ugly code
        if i%image.width != image.width-1:
            pixels[i+1] = tuple(numpy.round(numpy.add(pixels[i+1], error*errorR1)).astype(int))
            if i%image.width != image.width-2:
                pixels[i+2] = tuple(numpy.round(numpy.add(pixels[i+2], error*errorR2)).astype(int))
                if i+image.width+2 < len(pixels):
                    pixels[i+image.width+2] = tuple(numpy.round(numpy.add(pixels[i+image.width+2], error*(errorR2/2)).astype(int)))
                    if i+image.width*2+2 < len(pixels):
                        pixels[i+image.width*2+2] = tuple(numpy.round(numpy.add(pixels[i+image.width*2+2], error*(errorR2/3)).astype(int)))
            if i+image.width+1 < len(pixels):
                pixels[i+image.width+1] = tuple(numpy.round(numpy.add(pixels[i+image.width+1], error*errorR2).astype(int)))
                if i+image.width*2+1 < len(pixels):
                    pixels[i+image.width*2+1] = tuple(numpy.round(numpy.add(pixels[i+image.width*2+1], error*(errorR2/2)).astype(int)))
        if i+image.width < len(pixels):
            pixels[i+image.width] = tuple(numpy.round(numpy.add(pixels[i+image.width], error*errorR1).astype(int)))
            if i+image.width*2 < len(pixels):
                pixels[i+image.width*2] = tuple(numpy.round(numpy.add(pixels[i+image.width*2], error*errorR2).astype(int)))
    return pixels

def randomDither(image, colors, bias):
    pixels = list(image.getdata())
    for i in range(len(pixels)):
        distancesSum = 0
        colorDistances = []
        highestDistance = 0
        lowestDistance = 100000
        for j in range(len(colors)):
            distance = getDistance(pixels[i], colors[j])
            colorDistances.append(distance)
            if distance > highestDistance:
                highestDistance = distance
            if distance < lowestDistance:
                lowestDistance = distance
        for j in range(len(colors)):
            colorDistances[j] = (highestDistance+lowestDistance - colorDistances[j])**bias
            distancesSum += colorDistances[j]
        randNum = random.uniform(0, distancesSum)
        chosenId = 0
        dSum = 0
        for j in range(len(colors)):
            if dSum+colorDistances[j] >= randNum and randNum >= dSum:
                chosenId = j
                break
            dSum += colorDistances[j]
        pixels[i] = colors[chosenId]
    return pixels
