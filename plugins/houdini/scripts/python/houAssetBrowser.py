import hou

try:
    from jsAssetBrowser.api import assetBrowser
except ModuleNotFoundError:
    # Note:
    # houdini 19.0.455 has a problem that PYTHONPATH append in the package json dosnt work
    # this is a work around by manually adding this to the python path
    import sys
    sys.path.append("{}/python".format(hou.getenv("jsAssetBrowser")))
    from jsAssetBrowser.api import assetBrowser
    
# DEBUG
from importlib import reload

reload(assetBrowser)
#reload(qtUtils)
# DEBUG

"""
Module for the Houdini Asset Browser UI
"""


class HouAssetBrowser(assetBrowser.AssetBrowser):
    def __init__(self):
        super(HouAssetBrowser, self).__init__()

    def asset_clicked(self):
        caller = self.sender().objectName()
        print(caller)