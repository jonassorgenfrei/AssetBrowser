import os

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt


from jsAssetBrowser.ui import fontAwesome_icons_rc

class AssetItemInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super(AssetItemInfoWidget, self).__init__()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        
        # label
        self.name_lbl = QtWidgets.QLabel("Asset Name")
        self.name_lbl.setStyleSheet("font-weight: bold")
        
        self.tags_lbl = QtWidgets.QLabel("Tags")
        self.tags_lbl.setStyleSheet("font-weight: bold")
        
        self.similarAssets_lbl = QtWidgets.QLabel("Similar Assets")
        self.similarAssets_lbl.setStyleSheet("font-weight: bold")
        
        
        self.res_cb = QtWidgets.QComboBox()
        self.res_cb.addItems(["1k", "2k", "4k", "8k", "16k"])
        self.res_cb.currentIndexChanged.connect(self.resChanged)
        
        self.ext_cb = QtWidgets.QComboBox()
        self.ext_cb.addItems(["hdr", "exr"])
        self.ext_cb.currentIndexChanged.connect(self.extensionChanged)
        
        self.spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) 
        
        self.applyBtn = QtWidgets.QPushButton("Apply")
        
        mainLayout.addWidget(self.name_lbl)
        mainLayout.addWidget(self.tags_lbl)
        mainLayout.addWidget(self.similarAssets_lbl)
        mainLayout.addItem(self.spacer)
        mainLayout.addWidget(self.res_cb)
        mainLayout.addWidget(self.ext_cb)
        mainLayout.addWidget(self.applyBtn)
        
        self.setLayout(mainLayout)         
        
        # data
        self.assetItem = None
        
        self.resolution = "1k"
        self.extension = "hdr"
        
    def setAssetItem(self, assetItem):
        self.assetItem = assetItem
                
        self.name_lbl.setText(assetItem.name)
        
    def resChanged(self):
        self.resolution = self.res_cb.currentText()
        
    def extensionChanged(self):
        self.extension = self.ext_cb.currentText()