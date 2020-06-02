import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2 as cv
import math
import os
import numpy as np
import sys
from PIL import Image
class getLines():
    def __init__(self, img):
        self.path='%s\\%s'%(os.getcwd(),img)
        self.src = cv.imread(cv.samples.findFile(self.path), cv.IMREAD_GRAYSCALE)
        self.size=self.src.shape
        # Check if image is loaded fine
        if self.src is None:
            print('Error opening image!')
            print('Usage: hough_lines.py [image_name -- default ' + self.path+ '] \n')
            return -1

        self.dst = cv.Canny(self.src, 50, 200, None, 3)

        # Copy edges to the images that will display the results in BGR
        self.cdst = cv.cvtColor(self.dst, cv.COLOR_GRAY2BGR)

        self.lines = cv.HoughLines(self.dst, 1, np.pi / 180, 150, None, 0, 0)
    def getPath(self):
        return self.path
    def getSize(self):
        return self.size
    def getHorizontals(self):
        out=[]
        width=self.getSize()[0]
        for i in range(len(self.lines)):
            rho = self.lines[i][0][0]
            theta = self.lines[i][0][1]
            out.append(int(math.cos(theta)*rho))
        out.sort()
        x=0
        while x < len(out)-1:
            if out[x]==out[x+1]:
                out.pop(x+1)
            if abs(out[x]-out[x+1])<(width//9-int((width//9)*.1)):
                out.pop(x+1)
            else:
                x+=1
        return out
    def getVerticles(self):
        out=[]
        height=self.getSize()[1]
        for i in range(len(self.lines)):
            rho = self.lines[i][0][0]
            theta = self.lines[i][0][1]
            out.append(int(math.sin(theta)*rho))
        out.sort()
        x=0
        while x < len(out)-1:
            if out[x]==out[x+1]:
                out.pop(x+1)
            if abs(out[x]-out[x+1])<(height//9-int((height//9)*.1)):
                out.pop(x+1)
            else:
                x+=1
        return out
    def getIntersection(self):
        out=[]
        for x in self.getHorizontals():
            temp=[]
            for y in self.getVerticles():
                temp.append([x,y])
            out.append(temp)
        return out
    def getBlocks(self):
        out=[]
        for x in range(len(self.getIntersection())-1):
            for y in range(len(self.getIntersection()[0])-1):
                temp=[]
                temp.append(self.getIntersection()[x][y])
                temp.append(self.getIntersection()[x+1][y+1])
                out.append(temp)
        return out
    def getLines(self):
        lines=self.lines
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho

                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                print(pt1)
                cv.line(self.cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

        cv.imshow("Source", self.path)
        cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", self.cdst)

        cv.waitKey()
        return 0

a=getLines('sudoku.png')
print(a.getSize())

for x in a.getIntersection():
    print(x)
for y in a.getBlocks():
    print(y)
    c+=1

img=Image.open(a.getPath())
plt.imshow(img)
plt.show()