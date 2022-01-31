import nuke
from nukescripts import panels

from jsAssetBrowser.api import assetBrowser

class NukeAssetBrowser(assetBrowser.AssetBrowser):
    def __init__(self):
        super(NukeAssetBrowser, self).__init__()
    
    def asset_clicked(self):
        print("DATA - Nuke!")