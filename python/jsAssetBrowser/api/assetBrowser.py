"""
QT Implementation of the Asset Browser
"""

import os
import json
import pathlib
import time

from jsAssetBrowser.api import config, database, modules, online_requests
from jsAssetBrowser.api.assetBrowserTypes import AssetBrowserTypes
from urllib.request import Request, urlopen

from PySide2 import QtCore, QtNetwork

# DEBUG
from importlib import reload

reload(modules)
reload(database)
reload(config)
# DEBUG


# class syntax


dirname = os.path.dirname(__file__)
uiFile = "jsAssetBrowser.ui"


class AssetBrowser:
    def __init__(self):
        """Asset Browser Main Modul"""
        self.config = config.Config()

        self.db = database.Database(self.config)

        # Loading Plugins
        with open("{}/../plugins/plugins.json".format(dirname), "r") as f:
            pluginsNames = json.load(f)

        self.plugins = modules.loadPlugins(pluginsNames["plugins"])
        # Finished Plugin Loading

        thumb_height = 256
        thumb_width = int(thumb_height + thumb_height * 0.33333)-6

        self.thumbnailSize = QtCore.QSize(thumb_width, thumb_height)

        self.cached_assets = self.db.getAllImagesInDB(self.thumbnailSize)
        self.cached_thumbnails = self.db.getCachedThumbnails(
            self.thumbnailSize)
        
        # init
        self.type = AssetBrowserTypes.HDRIS
        self.category = None

    def changeType(self, type):
        """Changes the current state of the AssetBrowser to the given type

        Args:
            type (AssetBrowserTypes): type
        """
        self.type = type

    def getCategories(self):
        """Fills the category context

        Returns:
            list(strings): The list of categories
        """
        filters = {"type": self.type}
        categories = self.plugins[0].getCategories(filters)
        return categories

    def getItems(self):
        filters = {"type": self.type }
        if self.category != None and self.category != "all":
            filters = {"type": self.type, "category": self.category}

        # todo replace qtnetwork & qt thread with non qt functions
        self.download_queue = QtNetwork.QNetworkAccessManager()
        self.threadpool = QtCore.QThreadPool()

        return self.plugins[0].getItems(filters)

    def assetClicked(self):
        """
        Interface for the button clicked
        """
        # clickedAsset = self.sender().parent().assetItem

        # self.infoWidget.setAssetItem(clickedAsset)

        # set asset info data
        # connect assetItem to assetItemWidget
        # self.toggleAssetInfo(action='show')
