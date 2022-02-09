import os
import sqlite3

from jsAssetBrowser.api import config

conn = None

class Database():
    def __init__(self, config):
        global conn
        
        self.config = config
        dbFile = os.path.join(self.config.dataBaseFolder, "assetBrowser.db")
        conn = sqlite3.connect(dbFile)
    