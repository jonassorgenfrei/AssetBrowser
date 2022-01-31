import sys
sys.path.append("D:/Documents/Development/AssetBrowser/src")

from jsAssetBrowser.api.online_requests import request

from PySide2 import QtWidgets, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

class MayaAssetBrowser(MayaQWidgetDockableMixin, assetBrowser.AssetBrowser):
    def __init__(self):
        super(MayaAssetBrowser, self).__init__()

        # It is crucial we set a unique object name as this is used internally by Maya
        self.setObjectName("MayaAssetBrowser")
        self.setWindowTitle("JS Asset Browser")
        
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

if __name__ == "__main__":
    myWindow = MayaAssetBrowser()
    myWindow.show(dockable=True)
