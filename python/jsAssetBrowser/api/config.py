import os

class Config():
    def __init__(self):
        dirname = os.path.dirname(__file__)
        workpath = os.path.dirname(os.path.dirname(os.path.dirname(dirname)))
        self.downloadFolder = os.path.join(workpath, "downloads")

        if not os.path.exists(self.downloadFolder):
            os.makedirs(self.downloadFolder)
        
        self.dataBaseFolder = os.path.join(workpath, "data")
        if not os.path.exists(self.dataBaseFolder):
            os.makedirs(self.dataBaseFolder)