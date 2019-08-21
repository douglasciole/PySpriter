#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from tkinter.filedialog import askdirectory
import _tkinter
from Modules.Sprite import Sprite
import sys, os, time, math
from threading import Thread

class Window():

    def __init__(self):
        self.master = Tk()

        self.mode_folder = BooleanVar()
        self.mode_folder.set(True)
        self.sprite = None

        #Preview animation
        self.selectedAnimation = None
        self.animationList = []
        self.animationFrame = 0
        self.canAnimate = False
        self.thread = None

        self.addTopMenu()
        self.drawElements()

        self.master.title('Teste')
        self.master.geometry("800x600")
        self.master.minsize(800, 600)
        self.master.mainloop()

    def drawElements(self):
        self.buttonFrame()
        self.contentFrame()

    def buttonFrame(self):
        styleFrame1 = ttk.Style()
        styleFrame1.configure('TFrame', background='#8db3ef')

        self.frame1 = ttk.Frame(self.master, style='TFrame', padding=(5, 5, 5, 5))
        self.frame1.pack(fill=X, expand=False)

        ###
        self.FrameInfos = ttk.Labelframe(self.frame1, text='Infos', padding=(5, 8, 5, 10))
        self.FrameInfos.pack(fill=X, expand=YES, side=TOP, anchor=NW)

        labelDirLabel = ttk.Label(self.FrameInfos, text="DIR: ")
        labelDirLabel.pack(side=LEFT)
        self.labelDir = ttk.Label(self.FrameInfos, text="--> NOT SELECTED <--")
        self.labelDir.pack(side=LEFT)

        sep = ttk.Label(self.FrameInfos, text=" | ")
        sep.pack(side=LEFT)

        imageDimensionLabel = ttk.Label(self.FrameInfos, text="DIMENSION: ")
        imageDimensionLabel.pack(side=LEFT)
        self.imageDimension = ttk.Label(self.FrameInfos, text="[0x0]")
        self.imageDimension.pack(side=LEFT)

        sep2 = ttk.Label(self.FrameInfos, text=" | ")
        sep2.pack(side=LEFT)

        numberOfFilesLabel = ttk.Label(self.FrameInfos, text="Number of Files: ")
        numberOfFilesLabel.pack(side=LEFT)
        self.numberOfFiles = ttk.Label(self.FrameInfos, text="0")
        self.numberOfFiles.pack(side=LEFT)

        ###
        self.optionFrame = ttk.Labelframe(self.frame1, text='Folder Options', padding=(5, 8, 5, 10))
        self.optionFrame.pack(fill=X, expand=YES, side=TOP, anchor=W)

        self.modeFolder = ttk.Checkbutton(self.optionFrame, text="Each animation in a subfolder in selected folder´s root.", variable=self.mode_folder, onvalue=True, command=self.clearApplication)
        self.modeFolder.pack(side=LEFT, fill=None, expand=False)

        ###
        self.qualityOptionFrame = ttk.Labelframe(self.frame1, text='Quality Options', padding=(5, 0, 5, 0))
        self.qualityOptionFrame.pack(fill=X, expand=YES, side=TOP, anchor=W)

        columnNumberLabel = ttk.Label(self.qualityOptionFrame, text="Columns number: ")
        columnNumberLabel.pack(side=LEFT)
        self.columnNumber = Scale(self.qualityOptionFrame, from_=0, to=0, orient=HORIZONTAL)
        self.columnNumber.pack(side=LEFT)
        self.columnNumber.set(0)

        sep3 = ttk.Label(self.qualityOptionFrame, text=" | ")
        sep3.pack(side=LEFT)

        resizeLabel = ttk.Label(self.qualityOptionFrame, text="Resize(width): ")
        resizeLabel.pack(side=LEFT)
        self.resize = Scale(self.qualityOptionFrame, from_=0, to=0, orient=HORIZONTAL)
        self.resize.pack(side=LEFT)
        self.resize.set(0)

        sep4 = ttk.Label(self.qualityOptionFrame, text=" | ")
        sep4.pack(side=LEFT)

        reduceNumberOfFrameLabel = ttk.Label(self.qualityOptionFrame, text="Reduce frames between frames: ")
        reduceNumberOfFrameLabel.pack(side=LEFT)
        self.reduceNumberOfFrame = Scale(self.qualityOptionFrame, from_=0, to=10, orient=HORIZONTAL)
        self.reduceNumberOfFrame.pack(side=LEFT)
        self.reduceNumberOfFrame.set(0)


    def contentFrame(self):
        styleOpetion = ttk.Style()
        styleOpetion.configure('My.TFrame', background='#8db300')

        self.contentFrame = ttk.Frame(self.master, style='My.TFrame', padding=(5, 8, 5, 10))
        self.contentFrame.pack(fill=BOTH, expand=True)

        self.frame1 = ttk.Labelframe(self.contentFrame, text='Animation List', padding=(5, 5, 5, 5))
        self.frame1.pack(fill=BOTH, expand=False, side=LEFT, anchor=W)

        scrollbar = Scrollbar(self.frame1)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.frame1, width=45, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.listbox.bind('<<ListboxSelect>>', self.animatioSelect)
        scrollbar.config(command=self.listbox.yview)

        ###
        self.frame2 = ttk.Labelframe(self.contentFrame, text='Animation preview', padding=(5, 5, 5, 5))
        self.frame2.pack(fill=BOTH, expand=YES, side=LEFT, anchor=W)

        self.imagePreviw = Label(self.frame2, width=60)
        self.imagePreviw.pack(side=LEFT, fill=BOTH, expand=YES, anchor=W)

    def _ANIMATE(self):
        for sprite in self.sprite.images[self.listbox.get(self.listbox.curselection()[0])]:
            self.animationList.append(self.previewImageReduce(Image.open(sprite)))

        self.canAnimate = True

        while(self.canAnimate):
            self.preview(self.animationList[self.animationFrame])
            self.animationFrame += 1
            if (self.animationFrame > len(self.animationList)-1):
                self.animationFrame = 0
            time.sleep(0.07)



    def animatioSelect(self, event):
        if (len(self.listbox.curselection()) and self.selectedAnimation != self.listbox.curselection()):
            self.finishAnimation()
            
            self.selectedAnimation = self.listbox.curselection()
            self.animationList = []
            self.animationFrame = 0
            
            self.thread = Thread(target = self._ANIMATE)
            self.thread.daemon = True
            self.thread.start()

    def previewImageReduce(self, image):
        basewidth = 300
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def preview(self, photo):
        self.imagePreviw.configure(image=photo)
        self.imagePreviw.image = photo
        
    def removeAnimation(self):
        if (len(self.listbox.curselection())):
            if (self.mode_folder.get()):
                actualSize = self.sprite.removeFromAnimation(self.listbox.get(self.listbox.curselection()[0]))
                self.listbox.delete(self.listbox.curselection()[0])
                if (actualSize <= 0):
                    self.clearApplication()
            else:
                self.clearApplication()
        else:
            messagebox.showinfo("Alert", "Select a animation you want to remove from the list.")

    def addTopMenu(self):
        menuBar = Menu(self.master)
        
        fileMenuItem = Menu(menuBar, tearoff=False)
        fileMenuItem.add_command(label='Select Folder', command=self.selectDir)
        fileMenuItem.add_command(label='Generate', command=self.saveImage)
        fileMenuItem.add_separator()
        fileMenuItem.add_command(label='Clear', command=self.clearApplication)
        fileMenuItem.add_separator()
        fileMenuItem.add_command(label='Exit', command=self.extCommand)

        animMenuItem = Menu(menuBar, tearoff=False)
        animMenuItem.add_command(label='Remove selected', command=self.removeAnimation)

        menuBar.add_cascade(label='File', menu=fileMenuItem)
        menuBar.add_cascade(label='Animation', menu=animMenuItem)

        self.master.config(menu=menuBar)

    def saveImage(self):
        if (self.sprite is None):
            messagebox.showinfo("Alert", "Select a folder with images.")
            self.clearApplication()
        else:
            if (self.sprite.validDir):
                ftypes = [('Image Files', '*.png')]
                name=filedialog.asksaveasfile(filetypes=ftypes, defaultextension=".png")
                if (name != None):
                    self.sprite.generate(name.name, self.columnNumber.get(), self.resize.get())
            else:
                messagebox.showinfo("Alert", "Select a folder with images.")
                self.clearApplication()
            
    #Future feature
    def selectFile(self):
        self.master.filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("png files","*.png"), ("any file","*.*")))
        return self.master.filename

    def clearBtm(self):
        self.listbox.delete(0, END)

    def selectDir(self):
        self.finishAnimation()
        self.master.directory = askdirectory()
        if (self.master.directory != ""):
            self.sprite = Sprite(self.master.directory, self.mode_folder)
            
            if (self.sprite.validDir):
                self.selectedAnimation = -1
                self.updateInteractors()
                self.preview(self.previewImageReduce(Image.open(self.sprite.getFirstSprite())))
            else:
                self.clearApplication()

    def updateInteractors(self):
        #Sliders configuration
        self.columnNumber.config(from_=1, to=self.sprite.lenght)
        self.columnNumber.set(math.ceil(self.sprite.lenght / 3))
        self.resize.config(from_=math.ceil(self.sprite.width*0.1), to=self.sprite.width)
        self.resize.set(self.sprite.width)

        #Show informations about sprites
        self.numberOfFiles.config(text=str(self.sprite.lenght))
        self.labelDir.config(text=self.master.directory)
        self.imageDimension.config(text="["+str(self.sprite.width)+"x"+str(self.sprite.height)+"]")

        self.clearBtm()
        if (self.sprite.folderMode):
            for folder in self.sprite.folders:
                folder = folder.split("\\")
                self.listbox.insert(END, str(folder[len(folder)-2]))
        else:
            self.listbox.insert(END, str("Main"))

    def clearApplication(self):
        self.sprite = None
        self.clearBtm()

        self.finishAnimation()

        self.thread = None
        self.imagePreviw.configure(image='')
        self.imagePreviw.image = None

        #Sliders configuration
        self.columnNumber.config(from_=0, to=0)
        self.columnNumber.set(0)
        self.resize.config(from_=0, to=0)
        self.resize.set(0)

        #Show informations about sprites
        self.numberOfFiles.config(text="0")
        self.labelDir.config(text="--> NOT SELECTED <--")
        self.imageDimension.config(text="[0x0]")

    def finishAnimation(self):
        if (self.thread != None):
            self.canAnimate = False
            self.thread.join()

    def extCommand(self):
        sys.exit(0)