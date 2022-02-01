"""
QT Implementation of the Asset Browser
"""
import os
import json

from PySide2 import QtWidgets, QtGui, QtNetwork, QtCore, QtUiTools
from PySide2.QtCore import Qt
from jsAssetBrowser.api import modules
from jsAssetBrowser.api import online_requests
from jsAssetBrowser.api import qtUtils

from jsAssetBrowser.ui.flowLayout import FlowLayout
# qt load resources file
from jsAssetBrowser.ui import fontAwesome_icons_rc

# DEBUG
from importlib import reload
reload(modules)
reload(qtUtils)
# DEBUG

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
        self.fillItemArea()
       
    def changeTypeHdri(self):
        self.type = "hdris"
        self.fillItemArea()
        
    def changeTypeTexture(self):
        self.type = "textures"
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
        print(caller)