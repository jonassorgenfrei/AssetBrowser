"""
QT Implementation of the Asset Browser
"""
import os
import json
import pathlib
import time

# todo remove requests since nuke doest have this lib
try:
    import requests
except Exception:
    pass

from PySide2 import QtWidgets, QtGui, QtNetwork, QtCore, QtUiTools
from PySide2.QtCore import Qt
from jsAssetBrowser.api import modules
from jsAssetBrowser.api import online_requests
from jsAssetBrowser.api import qtUtils
from jsAssetBrowser.api.qtUtils import Worker

from jsAssetBrowser.ui.flowLayout import FlowLayout
# qt load resources file
from jsAssetBrowser.ui import fontAwesome_icons_rc

# DEBUG
from importlib import reload
reload(modules)
reload(qtUtils)
# DEBUG
from jsAssetBrowser.api.qtUtils import Worker

dirname = os.path.dirname(__file__)
uiFile = "jsAssetBrowser.ui"
thumbsize = 200

class AssetBrowser(QtWidgets.QWidget):
    def __init__(self):
        super(AssetBrowser, self).__init__()

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
        
        self.ui.contentSplitter.setStretchFactor(0, 0)
        self.ui.contentSplitter.setStretchFactor(1, 1)
        
        self.ui.itemSplitter.setStretchFactor(0, 1)
        self.ui.itemSplitter.setStretchFactor(1, 0)
        
        self.ui.contentLabel.setText("HDRIs")
        
        self.ui.modelBtn.clicked.connect(self.changeTypeModel)
        self.ui.hdriBtn.clicked.connect(self.changeTypeHdri)
        self.ui.textureBtn.clicked.connect(self.changeTypeTexture)
        
        self.assets_view = FlowLayout(self.flowWidget)
        
        self.type = "hdris"
        
        '''
        print(plugins[0].getFilters())
        '''
     
        self.fillItemArea()

        self.setLayout(mainLayout)

    def changeTypeModel(self):
        self.type = "models"
        self.ui.contentLabel.setText("Models")
        self.fillItemArea()
       
    def changeTypeHdri(self):
        self.type = "hdris"
        self.ui.contentLabel.setText("HDRIs")
        self.fillItemArea()
        
    def changeTypeTexture(self):
        self.type = "textures"
        self.ui.contentLabel.setText("Textures")
        self.fillItemArea()
    
    def fillItemArea(self):
        # clear asset view
        for i in reversed(range(self.assets_view.count())): 
            self.assets_view.itemAt(i).widget().setParent(None)
        
        filters = {"type": self.type }#"categorie": "skies"
        
        self.download_queue = QtNetwork.QNetworkAccessManager()
        self.threadpool = QtCore.QThreadPool()
        
        for item in self.plugins[0].getItems(filters):
            btn = QtWidgets.QToolButton()
            btn.setFixedSize(QtCore.QSize(thumbsize, thumbsize))
            btn.setIconSize(QtCore.QSize(thumbsize, thumbsize))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setText(item.name)
            btn.setObjectName("{}.{}".format(item.sourceKey, item.key))
 
            try:
                req = QtNetwork.QNetworkRequest(QtCore.QUrl(item.getIconURL(thumbsize)))
                down = qtUtils.ImgDownloader(btn, req)
                down.start_fetch(self.download_queue)
            except Exception as e:
                print(e)
            self.assets_view.addWidget(btn)
            
            btn.clicked.connect(self.asset_clicked)

    def asset_clicked(self):
        """Interface for the button clicked
        """
        caller = self.sender().objectName()
        caller = caller.replace("polyheaven.", "")
        print(caller)
        
    def requestFile(self, caller):
        
        resolution = "1k"
        ext = "hdr"
        
        hdr_json = json.loads(online_requests.request("https://api.polyhaven.com/files/{}".format(caller)))
        
        workpath = "D:/Documents/Development/AssetBrowser" # os.path.join(dirname, "..")
        
        
        self.url = hdr_json["hdri"][resolution][ext]["url"]
        self.file_size = hdr_json["hdri"][resolution][ext]["size"]
        local_file_name = pathlib.Path(workpath + "/downloads/" + os.path.basename(self.url))
        
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
    
    def download_img(self, progress_callback):
        # todo change requests to 
        res = requests.get(self.url, stream=True)
        offset = 0
        buffer = 512
        
        for chunk in res.iter_content(chunk_size=buffer):
            if not chunk:
                break
            
            self.local_file.seek(offset)
            self.local_file.write(chunk)
            offset = offset + len(chunk)
        
            progress = offset/int(self.file_size) * 100
            
            progress_callback.emit(progress)
        
        self.local_file.close()
        return "Done."
    
    def progress_fn(self, n):
        self.ui.progressBar.setValue(n)
        
    def print_output(self, s):
        print("Result:", s) 
        
    def thread_complete(self):
        print("Thread Done!")