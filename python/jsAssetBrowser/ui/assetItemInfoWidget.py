import os

from PySide2 import QtWidgets, QtCore, QtGui, QtNetwork
from PySide2.QtCore import Qt

from jsAssetBrowser.api import qtUtils
from jsAssetBrowser.ui.flowLayout import FlowLayout
from jsAssetBrowser.ui import fontAwesome_icons_rc


class AssetItemInfoWidget(QtWidgets.QWidget):
    def __init__(self):
        super(AssetItemInfoWidget, self).__init__()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # preview images
        self.previewImageStack = QtWidgets.QStackedWidget()

        # self buttons
        self.prevPreviewImage_btn = QtWidgets.QPushButton("<")
        self.nextPreviewImage_btn = QtWidgets.QPushButton(">")

        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(0, 0, 0, 0)
        btnLayout.addWidget(self.prevPreviewImage_btn)
        btnLayout.addWidget(self.nextPreviewImage_btn)

        self.prevPreviewImage_btn.clicked.connect(self.previousPreviewImage)
        self.nextPreviewImage_btn.clicked.connect(self.nextPreviewImage)
        
        # label
        self.name_lbl = QtWidgets.QLabel("Asset Name")
        self.name_lbl.setStyleSheet("font-weight: bold")

        self.tags_lbl = QtWidgets.QLabel("Tags:")

        # tags area
        self.tags_view = FlowLayout()

        self.similarAssets_lbl = QtWidgets.QLabel("Similar Assets:")

        self.res_cb = QtWidgets.QComboBox()
        self.res_cb.addItems(["1k", "2k", "4k", "8k", "16k"])
        self.res_cb.currentIndexChanged.connect(self.resChanged)

        self.ext_cb = QtWidgets.QComboBox()
        self.ext_cb.addItems(["hdr", "exr"])
        self.ext_cb.currentIndexChanged.connect(self.extensionChanged)

        self.spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.applyBtn = QtWidgets.QPushButton("Apply")

        mainLayout.addWidget(self.previewImageStack)
        mainLayout.addLayout(btnLayout)
        mainLayout.addWidget(self.name_lbl)
        mainLayout.addWidget(self.tags_lbl)
        mainLayout.addLayout(self.tags_view)
        mainLayout.addWidget(self.similarAssets_lbl)
        mainLayout.addItem(self.spacer)
        mainLayout.addWidget(self.res_cb)
        mainLayout.addWidget(self.ext_cb)
        mainLayout.addWidget(self.applyBtn)

        self.setLayout(mainLayout)

        # data
        self.assetItem = None
        self.currentPreview = 0

        self.resolution = "1k"
        self.extension = "hdr"

        self.download_queue = QtNetwork.QNetworkAccessManager()
        self.threadpool = QtCore.QThreadPool()

    def setAssetItem(self, assetItem):
        self.assetItem = assetItem
        self.currentPreview = 0
        self.name_lbl.setText(assetItem.name)

        # delete old preview images
        if self.previewImageStack.count() > 0:
            while self.previewImageStack.count():
                self.previewImageStack.removeWidget(self.previewImageStack.widget(0))

        for i, previewImgUrl in enumerate(assetItem.previews):
            print(previewImgUrl)
            previewImage = QtWidgets.QLabel()
            
            req = QtNetwork.QNetworkRequest(
                QtCore.QUrl(previewImgUrl)
            )
            
            down = qtUtils.ImgDownloader(previewImage, req)
            down.start_fetch(self.download_queue)
            
            self.previewImageStack.insertWidget(i, previewImage)

        qtUtils.clear_layout(self.tags_view)
        for tag in assetItem.tags:
            self.tags_view.addWidget(QtWidgets.QPushButton(tag))

    def nextPreviewImage(self):
        if self.assetItem:
            current_idx = self.previewImageStack.currentIndex()
            count_idxs = self.previewImageStack.count()
            self.previewImageStack.setCurrentIndex(current_idx + 1 if current_idx < count_idxs - 1 else 0)

    def previousPreviewImage(self):
        if self.assetItem:
            current_idx = self.previewImageStack.currentIndex()
            count_idxs = self.previewImageStack.count()
            self.previewImageStack.setCurrentIndex(current_idx - 1 if current_idx > 0 else count_idxs - 1)
            
    def resChanged(self):
        self.resolution = self.res_cb.currentText()

    def extensionChanged(self):
        self.extension = self.ext_cb.currentText()
