from PIL import Image
import math
import random
import colorsys
import numpy

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
    # todo: resize image to a small one, than get most common colors? 
    pixels = list(image.getdata())


def getDistance(color1, color2):
    return math.sqrt((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)

def threshold(image, colors):
    newImage = image.copy()
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
    newImage.putdata(pixels)
    return newImage

def dither2x2(image, colors, errorR1, errorR2):
    newImage = image.copy()
    pixels = list(newImage.getdata())
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
    newImage.putdata(pixels)
    return newImage

def randomDither(image, colors, bias):
    newImage = image.copy()
    pixels = list(newImage.getdata())
    for i in range(len(pixels)):
        #85000, 85400):
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
        #print(pixels[i], "=>", colors[chosenId], dSum, randNum, colorDistances, colors)
        pixels[i] = colors[chosenId]
    newImage.putdata(pixels)
    return newImage

def loadImage(path):
    try:
        original = Image.open(path)
    except:
        print("Unable to load image")
    original = original.convert("RGB")
    return original

#original = loadImage("gradient.png")
#original = loadImage("cat.jpeg")
original = loadImage("parrot.jpeg")
colors = getHSLColors(4, 1, 2)
#colors = getHSLColors(7, 1, 2) + getGreyscaleColors(2)
#colors = getGreyscaleColors(4)
randomDither(original, colors, 15).save("outputr.png")
threshold(original, colors).save("outputt.png")
dither2x2(original, colors, 1/4, 1/8).save("output2x2.png")
dither2x2(original, colors, 1/3, 1/5).save("output2x2t.png")
