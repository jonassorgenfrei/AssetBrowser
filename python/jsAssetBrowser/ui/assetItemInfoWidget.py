import os
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt


from jsAssetBrowser.ui import fontAwesome_icons_rc

class AssetItemInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super(AssetItemInfoWidget, self).__init__()
        
        self.assetItem = None
        
        
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        
        self.name_lbl = QtWidgets.QLabel("Asset")
        
        self.res_lbl = QtWidgets.QLabel("Resolution")
        self.res_cb = QtWidgets.QComboBox()
        self.res_cb.addItems(["1k", "2k", "4k", "8k", "16k"])
        self.res_cb.currentIndexChanged.connect(self.resChanged)
        
        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_cb = QtWidgets.QComboBox()
        self.ext_cb.addItems(["hdr", "exr"])
        self.ext_cb.currentIndexChanged.connect(self.extensionChanged)
        
        mainLayout.addWidget(self.name_lbl)
        mainLayout.addWidget(self.res_lbl)
        mainLayout.addWidget(self.res_cb)
        mainLayout.addWidget(self.ext_lbl)
        mainLayout.addWidget(self.ext_cb)
        self.setLayout(mainLayout)         
        
        # data
        self.resolution = "1k"
        self.extension = "hdr"
        
    def setAssetItem(self, assetItem):
        self.name_lbl.setText(assetItem.name)
        
    def resChanged(self):
        self.resolution = self.res_cb.currentText()
        
    def extensionChanged(self):
        self.extension = self.ext_cb.currentText()