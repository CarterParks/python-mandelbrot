#!python3
import colour 
from math import ceil
import sys
from PIL import Image
import random

# print out points of interest
INTEREST = False

class Mandelbrot:
    def __init__(self):
        self.z = complex(0.0,0.0)
        self.conf = {
                'width'     : 512,
                'height'    : 512,
                'centerx'   : 0.0,
                'centery'   : 0.0,
                'axislength': 0.25,
                'iterations': 100
            }

        self.centerSet()

    def count(self, c):
        z = self.z
        maxIter = int(self.getIterations())

        for i in range(maxIter):
            z = z * z + c
            if abs(z) > 2:
                if i == maxIter - 2 and INTEREST:
                    print(f'{c.imag},{c.imag}')
                return i + 1
        return maxIter

    def getIterations(self):
        return self.conf['iterations']

    def centerSet(self):
        with open('interest') as afile:
            line = random.choice(afile.readlines())

        line = line.split(',')
        self.conf['centerx'] = float(line[0])
        self.conf['centery'] = float(line[1])


class Pallette():
    def __init__(self, iterations):
        pallette = [
          '#8700ff',
          '#230051',
          '#fffffe',
          '#1c1c1c',
          '#0a0a0a',
        ]

        self.grad = []
        for n, h in enumerate(pallette[1:]):
            self.grad += list(colour.Color(pallette[n]).range_to(h, ceil(iterations/(2**(3-n)))))
            
    def getColor(self, n):
        return self.grad[n - 1]


def paint(fractal, gradient):
    fractalConf = fractal.conf

    BLACK = '#000000'
    WIDTH = int(fractalConf['width'])
    HEIGHT = int(fractalConf['height'])

    cx = float(fractalConf['centerx'])
    cy = float(fractalConf['centery'])
    al = float(fractalConf['axislength'])
    
    minx = cx - (al / 2.0)
    maxx = cx + (al / 2.0)
    miny = cy - (al / 2.0)
    maxy = cy + (al / 2.0)

    pixelW = abs(maxx - minx) / WIDTH
    pixelH = abs(maxy - miny) / HEIGHT

    imgArray = []

    # progress = 0

    for row in range(ceil(-HEIGHT/2), ceil(HEIGHT/2)):
        for col in range(ceil(-WIDTH/2), ceil(WIDTH/2)):

            # progress += 1
            # if progress % 1000 == 0:
                # print(str(ceil(100*progress/(WIDTH*HEIGHT))).zfill(2),end='%\r')
            
            x = cx + col * pixelW
            y = cy + row * pixelW

            c_z = complex(x, y)

            color = gradient.getColor(fractal.count(c_z))
            color = colour.hex2rgb(str(color))
            color = (int(255*color[0]), int(255*color[1]), int(255*color[2]))

            imgArray += [color]

    img = Image.new('RGB', (WIDTH, HEIGHT))
    img.putdata(imgArray)
    img.save('mandelbrot.png')

fractal = Mandelbrot()
gradient = Pallette(fractal.getIterations())

paint(fractal, gradient)
