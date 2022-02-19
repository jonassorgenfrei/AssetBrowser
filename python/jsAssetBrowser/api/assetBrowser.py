"""
QT Implementation of the Asset Browser
"""
from jsAssetBrowser.api.qtUtils import Worker
import os
import json
import pathlib
import time


from PySide2 import QtWidgets, QtGui, QtNetwork, QtCore, QtUiTools
from PySide2.QtCore import Qt

from jsAssetBrowser.api import config, database, modules, online_requests, qtUtils

from jsAssetBrowser.ui.flowLayout import FlowLayout
# qt load resources file
from jsAssetBrowser.ui import assetItemInfoWidget, assetItemWidget, fontAwesome_icons_rc
from urllib.request import Request, urlopen

# DEBUG
from importlib import reload
reload(modules)
reload(qtUtils)
reload(database)
reload(assetItemWidget)
reload(assetItemInfoWidget)
reload(config)
# DEBUG


dirname = os.path.dirname(__file__)
uiFile = "jsAssetBrowser.ui"


class AssetBrowser(QtWidgets.QWidget):
    def __init__(self):
        super(AssetBrowser, self).__init__()
        self.config = config.Config()

        self.db = database.Database(self.config)

        # Loading Plugins
        with open('{}/../plugins/plugins.json'.format(dirname), 'r') as f:
            pluginsNames = json.load(f)

        self.plugins = modules.loadPlugins(pluginsNames["plugins"])

        # Finished Plugin Loading

        # Load UI File
        self.loader = QtUiTools.QUiLoader()
        self.ui = self.loader.load(os.path.join(dirname, "..", "ui", uiFile))

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)

        # setup for flow layout
        self.flowWidget = QtWidgets.QWidget()
        self.ui.contentArea.setWidget(self.flowWidget)

        self.ui.contentSplitter.setStretchFactor(0, 1)
        self.ui.contentSplitter.setStretchFactor(1, 6)

        self.ui.itemSplitter.setStretchFactor(0, 4)
        self.ui.itemSplitter.setStretchFactor(1, 1)

        self.ui.itemSplitter.setSizes([2000, 0])

        self.ui.contentLabel.setText("HDRIs")

        self.ui.modelBtn.clicked.connect(self.changeTypeModel)
        self.ui.hdriBtn.clicked.connect(self.changeTypeHdri)

        self.ui.textureBtn.clicked.connect(self.changeTypeTexture)

        # btn to toggle item area
        self.ui.toggleItemAreaBtn.clicked.connect(
            lambda: self.toggleAssetInfo(action='toggle'))

        thumb_height = 256
        thumb_width = int(thumb_height + thumb_height * 0.33333)-6

        self.thumbnailSize = QtCore.QSize(thumb_width, thumb_height)

        self.cached_assets = self.db.getAllImagesInDB(self.thumbnailSize)
        self.cached_thumbnails = self.db.getCachedThumbnails(
            self.thumbnailSize)

        self.img_cached_assets = dict()

        self.assets_view = FlowLayout(self.flowWidget)
        self.assets_view.setSpacing(0)

        self.infoWidget = assetItemInfoWidget.AssetItemInfoWidget()
        self.ui.infoArea.setWidget(self.infoWidget)

        # init
        self.type = "hdris"
        self.category = None
        '''
        print(plugins[0].getFilters())
        '''

        self.fillItemArea()
        self.fillCategoriesArea()

        self.setLayout(mainLayout)

    def changeTypeModel(self):
        self.type = "models"
        self.ui.contentLabel.setText("Models")
        self.fillItemArea()
        self.fillCategoriesArea()

    def changeTypeHdri(self):
        self.type = "hdris"
        self.ui.contentLabel.setText("HDRIs")
        self.fillItemArea()
        self.fillCategoriesArea()

    def changeTypeTexture(self):
        self.type = "textures"
        self.ui.contentLabel.setText("Textures")
        self.fillItemArea()
        self.fillCategoriesArea()

    def changeCategory(self):
        caller = self.sender().objectName()
        if self.category != caller:
            self.category = caller
            self.fillItemArea()

    def fillCategoriesArea(self):
        filters = {"type": self.type}
        categories = self.plugins[0].getCategories(filters)

        # clear
        qtUtils.clear_layout(self.ui.categories)

        for category in categories:
            btn = QtWidgets.QPushButton(category)
            self.ui.categories.addWidget(btn)
            btn.setObjectName(category)
            btn.clicked.connect(self.changeCategory)

    def fillItemArea(self):
        # clear asset view
        qtUtils.clear_layout(self.assets_view)

        filters = {"type": self.type}  # "categorie": "skies"

        if self.category != None:
            filters = {"type": self.type,
                       "category": self.category}

        self.download_queue = QtNetwork.QNetworkAccessManager()
        self.threadpool = QtCore.QThreadPool()

        for item in self.plugins[0].getItems(filters):
            asset = assetItemWidget.AssetItemWidget(
                self.thumbnailSize, item.name, item.key, self.cached_assets)
            asset.setObjectName("{}.{}".format(item.sourceKey, item.key))

            if item.key in self.cached_thumbnails:
                #print("icons from data")
                asset.setIconFromData()
            else:
                req = QtNetwork.QNetworkRequest(QtCore.QUrl(
                    item.getIconURL(self.thumbnailSize.height())))

                down = qtUtils.ImgDownloader(asset, req)
                down.start_fetch(self.download_queue)

            self.assets_view.addWidget(asset)

            asset.btn.clicked.connect(self.asset_clicked)

    def asset_clicked(self):
        """Interface for the button clicked
        """
        caller = self.sender().parent().objectName()
        caller = caller.replace("polyheaven.", "")
        print(caller)

        # set asset info data
        # connect assetItem to assetItemWidget
        self.toggleAssetInfo(action='show')

    def requestFile(self, caller):
        resolution = self.infoWidget.resolution
        ext = self.infoWidget.extension

        hdr_json = json.loads(online_requests.request(
            "https://api.polyhaven.com/files/{}".format(caller)))

        self.url = hdr_json["hdri"][resolution][ext]["url"]
        self.file_size = hdr_json["hdri"][resolution][ext]["size"]
        local_file_name = pathlib.Path(os.path.join(
            self.config.downloadFolder, os.path.basename(self.url)))

        # check if file exists, it it does, skip download
        if not local_file_name.is_file():
            self.local_file = open(local_file_name, 'wb')

            # worker that downloads image
            worker = Worker(self.download_img)
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            self.threadpool.start(worker)

        return local_file_name

    def toggleAssetInfo(self, action='toggle'):
        splitter = self.ui.itemSplitter

        (left, right) = splitter.sizes()

        properties_default_size = 300
        if action == 'toggle':
            if right == 0:
                splitter.setSizes(
                    [left - properties_default_size, properties_default_size])
            else:
                splitter.setSizes([left + right, 0])
        elif action == 'show' and right == 0:
            splitter.setSizes(
                [left - properties_default_size, properties_default_size])

    def download_img(self, progress_callback):
        # todo change requests to
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})

        res = urlopen(req)
        offset = 0
        buffer = 512

        while True:
            chunk = res.read(buffer)
            if not chunk:
                break

            self.local_file.write(chunk)
            offset = offset + len(chunk)

            progress = offset/int(self.file_size) * 100

            progress_callback.emit(progress)

        progress_callback.emit(100)
        self.local_file.close()
        return "Done."

    def progress_fn(self, n):
        self.ui.progressBar.setValue(n)

    def print_output(self, s):
        print("Result:", s)

    def thread_complete(self):
        print("Thread Done!")
