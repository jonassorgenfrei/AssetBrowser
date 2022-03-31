import os
import pathlib

from urllib.request import Request, urlopen

from PySide2 import QtWidgets, QtCore, QtGui, QtNetwork
from PySide2.QtCore import Qt

from jsAssetBrowser.api import qtUtils
from jsAssetBrowser.api.qtUtils import AssetBrowserWorker
from jsAssetBrowser.ui.flowLayout import FlowLayout
from jsAssetBrowser.ui import fontAwesome_icons_rc, assetItemWidget


class AssetItemInfoWidget(QtWidgets.QWidget):
    def __init__(self, config,progressbar, cached_assets, cached_tumbnails):
        super(AssetItemInfoWidget, self).__init__()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        self.config = config
        self.progressBar = progressbar
         
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
        
        # asset name label
        self.name_lbl = QtWidgets.QLabel("Asset Name")
        self.name_lbl.setStyleSheet("font-weight: bold")

        # tags area
        self.tags_lbl = QtWidgets.QLabel("Tags:")
        self.tags_view = FlowLayout()

        # similar assets
        self.similarAssets_lbl = QtWidgets.QLabel("Similar Assets:")
        self.similarAssets_view = FlowLayout()
        self.similarAssets_view.setSpacing(0)

        self.res_cb = QtWidgets.QComboBox()
        self.res_cb.addItems(["1k", "2k", "4k", "8k", "16k"])
        self.res_cb.currentIndexChanged.connect(self.resChanged)

        self.ext_cb = QtWidgets.QComboBox()
        self.ext_cb.addItems(["hdr", "exr"])
        self.ext_cb.currentIndexChanged.connect(self.extensionChanged)

        self.spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.download_btn = QtWidgets.QPushButton("Download")
        self.download_btn.clicked.connect(self.downloadAssetItem)
        self.download_btn.setDisabled(True)

        mainLayout.addWidget(self.previewImageStack)
        mainLayout.addLayout(btnLayout)
        mainLayout.addWidget(self.name_lbl)
        mainLayout.addWidget(self.tags_lbl)
        mainLayout.addLayout(self.tags_view)
        mainLayout.addWidget(self.similarAssets_lbl)
        mainLayout.addLayout(self.similarAssets_view)
        mainLayout.addItem(self.spacer)
        mainLayout.addWidget(self.res_cb)
        mainLayout.addWidget(self.ext_cb)
        mainLayout.addWidget(self.download_btn)

        self.setLayout(mainLayout)

        # data
        self.assetItem = None
        self.currentPreview = 0
        self.cached_assets = cached_assets
        self.cached_thumbnails = cached_tumbnails
        self.resolution = "1k"
        self.extension = "hdr"

        self.download_queue = QtNetwork.QNetworkAccessManager()
        self.threadpool = QtCore.QThreadPool()

    def downloadAssetItem(self):
        url, file_size = self.assetItem.getDownloadLinks(self.resolution, self.extension)
        
        local_file_name = pathlib.Path(os.path.join(
            self.config.downloadFolder, os.path.basename(url)))

        # check if file exists, it it does, skip download
        if not local_file_name.is_file():
            self.local_file = open(local_file_name, 'wb')

            # worker that downloads image
            worker = AssetBrowserWorker(self.download_img, url, file_size)
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            self.threadpool.start(worker)

        return local_file_name
        
    def progress_fn(self, n):
        if self.progressBar.isHidden():
            self.progressBar.show()
        self.progressBar.setValue(n)
        
        if n >= 100:
            self.progressBar.hide()

    def print_output(self, s):
        print("Result:", s)

    def thread_complete(self):
        print("Thread Done!")

    def download_img(self, url, file_size, progress_callback):
        # todo change requests to
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        res = urlopen(req)
        offset = 0
        buffer = 512

        while True:
            chunk = res.read(buffer)
            if not chunk:
                break

            self.local_file.write(chunk)
            offset = offset + len(chunk)

            progress = offset/int(file_size) * 100

            progress_callback.emit(progress)

        progress_callback.emit(100)
        self.local_file.close()
        return "Done."

    def setAssetItem(self, assetItem):
        self.assetItem = assetItem
        self.currentPreview = 0
        self.name_lbl.setText(assetItem.name)

        # self only enable if not existing yet
        self.download_btn.setDisabled(False)
        
        self.setSimilarAssets()
        
        # delete old preview images
        if self.previewImageStack.count() > 0:
            while self.previewImageStack.count():
                self.previewImageStack.removeWidget(self.previewImageStack.widget(0))

        for i, previewImgUrl in enumerate(assetItem.previews):
            previewImage = QtWidgets.QLabel()
            
            req = QtNetwork.QNetworkRequest(
                QtCore.QUrl(previewImgUrl)
            )
            
            down = qtUtils.ImgDownloader(previewImage, req)
            down.start_fetch(self.download_queue)
            
            self.previewImageStack.insertWidget(i, previewImage)

        qtUtils.clear_layout(self.tags_view)
        for tag in assetItem.tags:
            tag_btn = QtWidgets.QPushButton(tag)
            # todo check css
            tag_btn.setStyleSheet("QPushButton{"
                                  "background-color: rgb(61, 61, 61);"
                                  "color: rgb(255, 255, 255);"
                                  "border: 2px solid #333;"
                                  "border-radius: 20px;}"
                                  "QPushButton::hover{"
                                  "background-color: rgb(30, 30, 30);}"
                                  "QPushButton::pressed{"
                                  "background-color: rgb(0, 255, 255);"
                                  "color: rgb(0,0,0);"
                                  "border: 2px solid #555;}")
            self.tags_view.addWidget(tag_btn)

    def setSimilarAssets(self):
        similarAssets = self.assetItem.getSimilarAssets()
        
        similarSize = QtCore.QSize(100, 100)
        qtUtils.clear_layout(self.similarAssets_view)
        
        for item in similarAssets:
            asset = assetItemWidget.AssetItemWidget(similarSize, 
                                                    item, 
                                                    self.cached_assets)
            
            asset.setObjectName("{}.{}".format(item.plugin.srcKey, item.key))

            if item.key in self.cached_thumbnails:
                asset.setIconFromData()
            else:
                req = QtNetwork.QNetworkRequest(QtCore.QUrl(
                    item.getIconURL(self.thumbnailSize.height())))

                down = qtUtils.ImgDownloader(asset, req)
                down.start_fetch(self.download_queue)

            self.similarAssets_view.addWidget(asset)

            asset.btn.clicked.connect(self.similarAsset_clicked)

    def similarAsset_clicked(self):
        clickedAsset = self.sender().parent().assetItem
        
        self.setAssetItem(clickedAsset)
    
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
