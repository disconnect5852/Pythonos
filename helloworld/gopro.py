from goprocam import GoProCamera, constants
import tkinter as tk
from tkinter import filedialog
import pygubu
import json
import datetime
import numpy as np
import threading
import time
import asyncio


class GauPrauHandler:
    goproCamera = GoProCamera.GoPro()

    def __init__(self, invoker):
        self.invoker = invoker
        self.clsmedialist = list()
        # th = threading.Thread(target=self.keepHopeAlive)
        # th.start()
        print("hendl")

    def listMedia(self):
        # self.goproCamera.KeepAlive()
        rawdata = self.goproCamera.listMedia(False, True)
        # f = open("mediaz.txt", "a")
        # f.write(rawdata)
        # f.close()
        media = (json.loads(rawdata))["media"]
        thelist = list()
        self.clsmedialist=thelist
        for folder in media:
            foldername = folder["d"]
            print(foldername)
            for ting in folder["fs"]:
                creationtime = datetime.datetime.fromtimestamp(int(ting["cre"]))
                # self.invoker.medialist.insert(tk.END, (foldername, time, ting["n"]))
                thelist.append((foldername, ting["n"], creationtime))
        print("listing media")
        return thelist

    def downMedia(self, selection,selectdir):
        print(selection, selectdir)
        # selectarr = [i[1] for i in selection]
        selectarr = [self.clsmedialist[idx] for idx in selection]
        for dikk in selectarr:
            print(dikk[0], dikk[1])
            self.goproCamera.downloadMedia(dikk[0], dikk[1])



class GauPrauGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.handler = GauPrauHandler(self)
        listbutton = tk.Button(text="nyomjad", command=self.fillListbocks)
        downbutton = tk.Button(text="dánlód", command=self.downloadselected)
        listbutton.pack()
        downbutton.pack()
        self.medialist = tk.Listbox(selectmode=tk.MULTIPLE, width=60)
        self.medialist.pack()
        clearbutton = tk.Button(text="kijelöléstörlés", command=self.clearselection)
        clearbutton.pack()
        # self.window.protocol("WM_DELETE_WINDOW", self.kloze())
        self.window.mainloop()

    def fillListbocks(self):
        dalist = self.handler.listMedia()
        self.medialist.insert(tk.END, *dalist)
        
    def clearselection(self):
        self.medialist.selection_clear(0, tk.END)

    def downloadselected(self):
        selected= self.medialist.curselection()
        selectdir= filedialog.askdirectory(title="jelöljed ki hova")
        self.handler.downMedia(selected, selectdir)



# goproCamera = GoProCamera.GoPro()
# mediaz= goproCamera.listMedia(False,True)

# for media in mediaz:
# print (media)
# print(mediaz)
# goproCamera.downloadMedia("100GOPRO","GH014107.MP4");

gui = GauPrauGUI()
