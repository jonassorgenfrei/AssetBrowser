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
        conn.execute("""CREATE TABLE IF NOT EXISTS thumbnails (name TEXT PRIMARY KEY, size INTEGER, img BLOB)""")
        
    def insertImg(self, name, size, img_data):
        global conn
        
        sql = """INSERT INTO thumbnails (name, size, img) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET size = excluded.size, img = excluded.img"""
        
        data = (name, size, img_data)
        conn.execute(sql, data)
        conn.commit()
    
    def getCachedThumbnails(self, thumbsize):
        global conn 
        
        existing_assets = conn.execute('''SELECT name from thumbnails WHERE size=?''',
                                      (thumbsize.height(),)).fetchall()
        
        existing_assets = [x[0] for x in existing_assets]
        
        return existing_assets

    def getAllImagesInDB(self, thumbsize):
        global conn
        global cached_assets
        
        conn.row_factory = sqlite3.Row
        
        cached_imgs = conn.execute('''SELECT name, img FROM thumbnails WHERE size=?''',
                                  (thumbsize.height(), )).fetchall()
        
        for row in cached_imgs:
            cached_assets[row['name']] = row['img']
        
        return cached_assets


# TODO only temporarily
# db = database.Database(config.Config())
# db.insertImg("houdini", 256, img_binary)