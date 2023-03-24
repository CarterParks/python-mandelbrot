#!python3
import colour 
from math import ceil
import sys
from PIL import Image
from random import randrange

class Mandelbrot:
    def __init__(self):
        self.z = complex(0.0,0.0)
        self.conf = {
                'width'     : 1440,
                'height'    : 900,
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
                # if i == maxIter - 2:
                    # self.write(c)
                return i + 1
        return maxIter

    def getIterations(self):
        return self.conf['iterations']

    def write(self, c):
        c = str(c).replace(')','#').replace('j','#').replace('+','#,')
        c = c.replace('(-','#A').replace('-','#,-')
        c = c.replace('A','#-').replace('(','#')
        print(c)
        
    def centerSet(self):
        with open('interest') as afile:
            line = next(afile)
            for num, aline in enumerate(afile, 2):
                if randrange(num): continue
                line = aline

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
    '''Paint a Fractal image into the TKinter PhotoImage canvas.
    This code creates an image which is 512x512 pixels in size.'''
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

    tot = 0

    for row in range(ceil(-HEIGHT/2), ceil(HEIGHT/2)):
        for col in range(ceil(-WIDTH/2), ceil(WIDTH/2)):

            tot += 1
            # if tot % 1000 == 0:
                # print(str(ceil(100*tot/(WIDTH*HEIGHT))).zfill(2),end='%\r')
            
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
