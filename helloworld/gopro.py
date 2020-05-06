from goprocam import GoProCamera, constants
import tkinter as tk
import json
import datetime
import threading
import time
import asyncio


class GauPrauHandler:
    goproCamera = GoProCamera.GoPro()

    def __init__(self, invoker):
        self.invoker = invoker
        #th = threading.Thread(target=self.keepHopeAlive)
        #th.start()
        print("hendl")

    def listMedia(self):
        #self.goproCamera.KeepAlive()
        rawdata= self.goproCamera.listMedia(False,True)
        # f = open("mediaz.txt", "a")
        # f.write(rawdata)
        # f.close()
        media=(json.loads(rawdata))["media"]
        thelist= list()
        for folder in media:
            foldername=folder["d"]
            print(foldername)
            for ting in folder["fs"]:
                time= datetime.datetime.fromtimestamp(int(ting["cre"]))
                #self.invoker.medialist.insert(tk.END, (foldername, time, ting["n"]))
                thelist.append((foldername, time, ting["n"]))
        print("listing media")
        print(thelist)
        return thelist


class GauPrauGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.handler = GauPrauHandler(self)
        listbutton = tk.Button(text="nyomjad", command=self.fillListbocks)
        self.medialist = tk.Listbox(selectmode=tk.MULTIPLE)
        listbutton.pack()
        self.medialist.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.kloze())
        self.window.mainloop()
    def fillListbocks(self):
        dalist= self.handler.listMedia()
        self.medialist.insert(tk.END,*dalist)

#goproCamera = GoProCamera.GoPro()
#mediaz= goproCamera.listMedia(False,True)

# for media in mediaz:
    # print (media)
# print(mediaz)
# goproCamera.downloadMedia("100GOPRO","GH014107.MP4");

gui = GauPrauGUI()
