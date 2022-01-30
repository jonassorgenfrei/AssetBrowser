import nuke
from nukescripts import panels

from jsAssetBrowser.api import assetBrowser
from jsAssetBrowser.api.online_requests import request

from PySide2 import QtWidgets, QtGui

class NukeAssetBrowser(assetBrowser.AssetBrowser):
    def __init__(self):
        super(NukeAssetBrowser, self).__init__()

        # Load UI File
        #loader = QtUiTools.QUiLoader()
        #self.ui = loader.load(UIFOLDER + UIFILE2)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        mainLayout.addWidget(QtWidgets.QPushButton("Button"))
        
        img = QtGui.QImage()
        img.loadFromData(request("https://cdn.polyhaven.com/asset_img/thumbs/oberer_kuhberg.png?height=200"))
        img_lbl = QtWidgets.QLabel("img")
        img_lbl.setPixmap(QtGui.QPixmap(img))
        mainLayout.addWidget(img_lbl)

        self.setLayout(mainLayout)
