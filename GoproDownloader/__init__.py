import datetime
import json
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar

from goprocam import GoProCamera


class GauPrauHandler:
    goproCamera = GoProCamera.GoPro()

    def __init__(self, invoker):
        self.invoker = invoker
        self.clsmedialist = list()
        # th = threading.Thread(target=self.keepHopeAlive)
        # th.start()
        keephopealive = threading.Thread(target=self.goproCamera.KeepAlive, args=())
        keephopealive.daemon = True
        keephopealive.start()
        print("hendl")

    def listMedia(self):
        # self.goproCamera.KeepAlive()
        rawdata = self.goproCamera.listMedia(False, True)
        # f = open("mediaz.txt", "a")
        # f.write(rawdata)
        # f.close()
        media = (json.loads(rawdata))["media"]
        self.clsmedialist = list()
        for folder in media:
            foldername = folder["d"]
            print(foldername)
            for ting in folder["fs"]:
                creationtime = datetime.datetime.fromtimestamp(int(ting["cre"]))
                # self.invoker.medialist.insert(tk.END, (foldername, time, ting["n"]))
                self.clsmedialist.append((foldername, ting["n"], creationtime))
        print("listing media")
        return self.clsmedialist

    def downMedia(self, selection, selectdir):
        print(selection, selectdir)
        selectarr = [self.clsmedialist[idx] for idx in selection]
        for dikk in selectarr:
            print(dikk[0], dikk[1])
            self.goproCamera.downloadMedia(dikk[0], dikk[1], selectdir + "/" + dikk[1])


class GauPrauGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GoPro media downloader")
        # self.progress = Progressbar(self.window, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.handler = GauPrauHandler(self)
        self.listbutton = tk.Button(text="List media", command=self.fillListbocks)
        self.downbutton = tk.Button(text="Download selected", command=self.downloadselected)
        self.listbutton.pack()
        self.downbutton.pack()
        self.medialist = tk.Listbox(selectmode=tk.MULTIPLE, width=60)
        self.medialist.pack()
        clearbutton = tk.Button(text="Clear selection", command=self.clearselection)
        clearbutton.pack()
        # self.window.protocol("WM_DELETE_WINDOW", self.kloze())
        self.window.mainloop()

    def fillListbocks(self):
        dalist = self.handler.listMedia()
        self.medialist.insert(tk.END, *dalist)

    def clearselection(self):
        self.medialist.selection_clear(0, tk.END)

    def downloadselected(self):
        selected = self.medialist.curselection()
        selectdir = filedialog.askdirectory(title="Select download folder")
        self.handler.downMedia(selected, selectdir)


gui = GauPrauGUI()
