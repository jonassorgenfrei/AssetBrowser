import hou


from PySide2 import QtWidgets, QtGui

try:
    from jsAssetBrowser.api import assetBrowser
    from jsAssetBrowser.api.online_requests import request
except ModuleNotFoundError:
    # Note:
    # houdini 19.0.455 has a problem that PYTHONPATH append in the package json dosnt work
    # this is a work around by manually adding this to the python path
    import sys
    sys.path.append("{}/src".format(hou.getenv("jsAssetBrowser")))
    from jsAssetBrowser.api import assetBrowser
    from jsAssetBrowser.api.online_requests import request
    
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
        img.loadFromData(request("https://cdn.polyhaven.com/asset_img/thumbs/oberer_kuhberg.png?height=200"))
        img_lbl = QtWidgets.QLabel("img")
        img_lbl.setPixmap(QtGui.QPixmap(img))
        mainLayout.addWidget(img_lbl)

        self.setLayout(mainLayout)
