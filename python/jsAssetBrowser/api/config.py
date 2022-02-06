import os

class Config():
    def __init__(self):
        dirname = os.path.dirname(__file__)
        workpath = os.path.dirname(os.path.dirname(os.path.dirname(dirname)))
        self.downloadFolder = os.path.join(workpath, "downloads")