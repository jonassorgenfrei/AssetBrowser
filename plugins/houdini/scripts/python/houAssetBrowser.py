import hou
import requests

from PySide2 import QtWidgets, QtUiTools, QtGui

from jsAssetBrowser.api import assetBrowser

# DEBUG
from importlib import reload
reload(assetBrowser)
# DEBUG

"""
Module for the Houdini Asset Browser UI
"""


class HouAssetBrowser(assetBrowser.AssetBrowser):
    def __init__(self):
        super(HouAssetBrowser, self).__init__()

        # Load UI File
        #loader = QtUiTools.QUiLoader()
        #self.ui = loader.load(UIFOLDER + UIFILE2)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        mainLayout.addWidget(QtWidgets.QPushButton("Button"))
        
        img = QtGui.QImage()
        img.loadFromData(requests.get("https://cdn.polyhaven.com/asset_img/thumbs/oberer_kuhberg.png?height=200").content)
        img_lbl = QtWidgets.QLabel("img")
        img_lbl.setPixmap(QtGui.QPixmap(img))
        mainLayout.addWidget(img_lbl)

        self.setLayout(mainLayout)
