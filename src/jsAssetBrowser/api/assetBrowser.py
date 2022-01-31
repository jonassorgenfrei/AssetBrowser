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
# DEBUG
from importlib import reload
reload(modules)
reload(qtUtils)
# DEBUG

dirname = os.path.dirname(__file__)
uiFile = "ui/jsAssetBrowser.ui"
thumbsize = 200

class AssetBrowser(QtWidgets.QWidget):
    def __init__(self):
        super(AssetBrowser, self).__init__()

        # Loading Plugins
        with open('{}/../plugins/plugins.json'.format(dirname), 'r') as f:
            pluginsNames = json.load(f)

        plugins = modules.loadPlugins(pluginsNames["plugins"])

        for plugin in plugins:
            plugin.run()

        # Finished Plugin Loading
        
        # Load UI File
        self.loader = QtUiTools.QUiLoader()
        self.ui = self.loader.load(os.path.join(dirname, "..", uiFile))

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        
        # setup for flow layout
        self.flowWidget = QtWidgets.QWidget()
        self.ui.contentArea.setWidget(self.flowWidget)
        
        assets_view = FlowLayout(self.flowWidget)

        
        
        '''
         try:
            print(plugins[0].getFilters())
        except Exception as e:
            print(e)
        '''
        
        filters = {"type": "hdris",
                   "categorie": "skies"}
        filters = {}
        
        self.download_queue = QtNetwork.QNetworkAccessManager()
        
        for item in plugins[0].getItems(filters):
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
            assets_view.addWidget(btn)
            
            btn.clicked.connect(self.asset_clicked)

        self.setLayout(mainLayout)

    def asset_clicked(self):
        """Interface for the button clicked
        """
        caller = self.sender().objectName()
        print(caller)