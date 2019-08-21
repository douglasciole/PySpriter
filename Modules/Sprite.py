#!/usr/bin/env python3
import glob, math, os
from PIL import Image
from tkinter import messagebox

class Sprite():

    def __init__(self, srcFolder, subfolderMode):
        if (os.path.exists(srcFolder)):
            self.sourceFolder = srcFolder
            self.validDir = False
            self.images = {}
            self.folderMode = subfolderMode.get()
            
            if (self.folderMode):
                self.folders = glob.glob(self.sourceFolder+"/*/")
                for folder in self.folders:
                    fName = folder.split("\\")
                    fName = str(fName[len(fName)-2])
                    self.images[fName] = []
                    self.images[fName] += glob.glob(folder+"/*.png")
                    if (len(self.images[fName]) <= 0):
                        del self.images[fName]
            else:
                self.images["Main"] = []
                self.images["Main"] += glob.glob(self.sourceFolder+"/*.png")
                if (len(self.images["Main"]) <= 0):
                        del self.images["Main"]

            self.lenght = self.count()
            if (self.lenght > 0):
                img1 = Image.open(self.getFirstSprite())
                self.width, self.height = img1.size
                self.validDir = True
            else:
                self.folderAlert()
                self.validDir = False

    def count(self):
        countQtd = 0
        for key in self.images:
            countQtd += len(self.images[key])
        return countQtd

    def getFirstSprite(self):
        return self.images[list(self.images)[0]][0]

    def folderAlert(self):
        if (self.folderMode):
            messagebox.showinfo("Alert", "[Folder mode: Each animation in one folder] - Select a folder with subfolders.")
        else:
            messagebox.showinfo("Alert", "[Folder mode: All images in one folder] - Select a folder with images in its root.")

    def removeFromAnimation(self, animationName):
        imgsTemp = []
        for image in self.images:
            if (not animationName in image):
                imgsTemp.append(image)
        self.images = imgsTemp

        return len(self.images)

    def generate(self, destinationFile, horizontalSize, newSize):
        if (self.validDir):
            if (self.lenght > 0):
                if (horizontalSize > self.lenght):
                    horizontalSize = self.lenght

                verticalSize = math.ceil(self.lenght/horizontalSize)

                coordenateX = 0
                coordenateY = 0
                _widthVal = self.width
                _heightVal = self.height
                _resize = False

                if (newSize != _widthVal):
                    _widthVal = newSize
                    wPercent = (_widthVal/float(self.width))
                    _heightVal = int((float(_heightVal)*float(wPercent)))
                    _resize = True


                try:
                    img = Image.new('RGBA',(horizontalSize*_widthVal, verticalSize*_heightVal))
                    for image in self.images:
                        imAtual = Image.open(image)
                        if (_resize):
                            imAtual = imAtual.resize((_widthVal,_heightVal), Image.ANTIALIAS)
                        
                        img.paste(imAtual, (coordenateX*_widthVal, coordenateY*_heightVal), imAtual)
                        coordenateX = coordenateX + 1
                        if (coordenateX >= horizontalSize):
                            coordenateX = 0
                            coordenateY = coordenateY + 1

                    img.save(destinationFile, 'PNG',optimize=True, quality=50)
                except:
                     messagebox.showinfo("Erro", "Please make sure you have administrator permission or all images are in the directory!")
                     self.validDir = False
        else:
            self.folderAlert()
            self.validDir = False