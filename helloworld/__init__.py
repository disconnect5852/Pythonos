import fnmatch
import os
import glob
from pathlib import Path


class Tesztolok:

    def __init__(self, lepath=None, lofilter=None, izfolder=False):
        self.folderz = os.scandir(lepath)
        self.pathz = Path(lepath if lepath is not None else "/")
        self.lofilter = lofilter
        self.izfolder = izfolder

    def fold(self):
        for wasd in self.folderz:
            print(wasd.name)

    def paths(self):
        for asd in self.pathz.iterdir():
            if (os.path.isdir(asd) if self.izfolder else True) and (self.lofilter in asd.name if self.lofilter is not None else True):
                print(asd.name)

lopett="e:/"
filtez="asd"

leclass = Tesztolok(lopett, filtez, False)
leclass.paths()

for currentpath, folders, files in os.walk(lopett):
    #folders[:] = [d for d in folders if "ash" in d]
    for file in folders:
        # print(os.path.join(currentpath, file))
        if filtez in file:
            print(file)

