from PySide2 import QtWidgets, QtGui, QtNetwork, QtCore, QtUiTools
import os

from jsAssetBrowser.ui.flowLayout import FlowLayout
# qt load resources file
from jsAssetBrowser.ui import assetItemInfoWidget, assetItemWidget, fontAwesome_icons_rc, qtUtils

from jsAssetBrowser.api.assetBrowserTypes import AssetBrowserTypes

# DEBUG
from importlib import reload
reload(assetItemWidget)
reload(assetItemInfoWidget)
reload(qtUtils)
# DEBUG

dirname = os.path.dirname(__file__)
uiFile = "jsAssetBrowser.ui"

class AssetBrowserWidget(QtWidgets.QWidget):
    """The main Ui for the asset browser

    Args:
        QtWidgets (_type_): _description_
    """
    def __init__(self, assetBrowser):
        super(AssetBrowserWidget, self).__init__()
        
        # asset browser api
        self.assetBrowser = assetBrowser
        
        # Load UI File
        self.loader = QtUiTools.QUiLoader()
        self.ui = self.loader.load(os.path.join(dirname, uiFile))
        
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        
        # setup for flow layout
        self.flowWidget = QtWidgets.QWidget()
        self.ui.contentArea.setWidget(self.flowWidget)

        self.ui.contentSplitter.setStretchFactor(0, 1)
        self.ui.contentSplitter.setStretchFactor(1, 6)

        self.ui.itemSplitter.setStretchFactor(0, 4)
        self.ui.itemSplitter.setStretchFactor(1, 1)

        self.ui.itemSplitter.setSizes([2000, 0])

        self.ui.contentLabel.setText("HDRIs")

        self.ui.modelBtn.clicked.connect(self.changeTypeModel)
        self.ui.hdriBtn.clicked.connect(self.changeTypeHdri)
        self.ui.textureBtn.clicked.connect(self.changeTypeTexture)

        self.ui.progressBar.hide()

        # btn to toggle item area
        self.ui.toggleItemAreaBtn.clicked.connect(
            lambda: self.toggleAssetInfo(action='toggle'))

        thumb_height = 256
        thumb_width = int(thumb_height + thumb_height * 0.33333)-6

        self.thumbnailSize = QtCore.QSize(thumb_width, thumb_height)

        self.img_cached_assets = dict()

        self.assets_view = FlowLayout(self.flowWidget)
        self.assets_view.setSpacing(0)

        self.infoWidget = assetItemInfoWidget.AssetItemInfoWidget(self.assetBrowser.config, 
                                                                  self.ui.progressBar,
                                                                  self.assetBrowser.cached_assets,
                                                                  self.assetBrowser.cached_thumbnails)
        self.ui.infoArea.setWidget(self.infoWidget)

        self.fillItemArea()
        self.fillCategoriesArea()

        self.setLayout(mainLayout)
        
    def changeTypeModel(self):
        self.assetBrowser.changeType(AssetBrowserTypes.MODELS)
        self.ui.contentLabel.setText("Models")
        self.fillItemArea()
        self.fillCategoriesArea()

    def changeTypeHdri(self):
        self.assetBrowser.changeType(AssetBrowserTypes.HDRIS)
        self.ui.contentLabel.setText("HDRIs")
        self.fillItemArea()
        self.fillCategoriesArea()

    def changeTypeTexture(self):
        self.assetBrowser.changeType(AssetBrowserTypes.TEXTURES)
        self.ui.contentLabel.setText("Textures")
        self.fillItemArea()
        self.fillCategoriesArea()

    def changeCategory(self):
        #caller = self.sender().objectName()
        #if self.category != caller:
        #    self.category = caller
        #    self.fillItemArea()
        pass
    
    '''
    def find_tag_in_assets(self):
        # connect tag button
        # tag_btn.clicked.connect(self.find_tag_in_assets)
        tag_name = self.sender().text()
        for asset in self.all_data():
            tags = self.all_data[asset]['tags']
            if tag_name in tags:
                self.tags_section[asset] = self.all_data[asset]
                
        self. load_assets_with_tag()
        
    def load_assets_with_tag(self):
        self.clear_layout(self.assets_view)
        for key in self.tags_selection.keys():
            asset = AssetItem(self.thumbsize, key)
            asset.setObjectName(key)
            url = "https://cdn.polyhaven.com/asset_img/thumbs/" + key + ".png?height="+str(self.thumbnailsize)
            req = QtNetwork.QNetworkRequest(QtCore.QUrl(ulr))
            self.assets_view.addWidget(asset)
            
            if key in self.cached_assets:
                asset.set_icon_from_data()
            else:
                down = ImgDownloader(asset, req)
                down.start_fetch(self.download_queue)
                
            #connect function to button
            asset.btn.clicked.connect(self.asset_clicked)
    '''
    
    def fillCategoriesArea(self):
        categories = self.assetBrowser.getCategories()
        # clear
        qtUtils.clear_layout(self.ui.categories)

        for category in categories:
            btn = QtWidgets.QPushButton(category)
            self.ui.categories.addWidget(btn)
            btn.setObjectName(category)
            btn.clicked.connect(self.changeCategory)

    def fillItemArea(self):
        # clear asset view
        qtUtils.clear_layout(self.assets_view)
        
        items = self.assetBrowser.getItems()

        for item in items:
            asset = assetItemWidget.AssetItemWidget(self.thumbnailSize, 
                                                    item, 
                                                    self.assetBrowser.cached_assets)
            asset.setObjectName("{}.{}".format(item.plugin.srcKey, item.key))

            if item.key in self.assetBrowser.cached_thumbnails:
                #print("icons from data")
                asset.setIconFromData()
            else:
                req = QtNetwork.QNetworkRequest(QtCore.QUrl(
                    item.getIconURL(self.thumbnailSize.height())))
                down = qtUtils.ImgDownloader(asset, req)
                down.start_fetch(self.assetBrowser.download_queue)

            self.assets_view.addWidget(asset)

            asset.btn.clicked.connect(self.asset_clicked)
            
    def asset_clicked(self):
        """Interface for the button clicked
        """
        clickedAsset = self.sender().parent().assetItem
        
        self.infoWidget.setAssetItem(clickedAsset)
        
        # set asset info data 
        # connect assetItem to assetItemWidget
        self.toggleAssetInfo(action='show')


    def toggleAssetInfo(self, action='toggle'):
        splitter = self.ui.itemSplitter

        (left, right) = splitter.sizes()

        properties_default_size = 600
        if action == 'toggle':
            if right == 0:
                splitter.setSizes(
                    [left - properties_default_size, properties_default_size])
            else:
                splitter.setSizes([left + right, 0])
        elif action == 'show' and right == 0:
            splitter.setSizes(
                [left - properties_default_size, properties_default_size])
