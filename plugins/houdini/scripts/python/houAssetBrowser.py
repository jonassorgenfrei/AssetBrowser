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
        caller = caller.replace("polyheaven.", "") 
        
        file = super().requestFile(caller)
        self.assign_hdr(file)
        
    def assign_hdr(self, file):
        # assign HDRI to selected item
        selItems = hou.selectedNodes()
        
        if len(selItems) > 0:
            selItem = selItems[0]
            
            nodeType = selItem.type().name()

            if nodeType == "envlight":
                # for environment light
                selItem.parm("env_map").set(str(file))
            elif nodeType == "rslightdome::2.0":
                # for redshift env light
                selItem.parm("env_map").set(str(file))
            elif nodeType == "arnold_light":
                selItem.parm("ar_light_type").set(6)
                selItem.parm("ar_light_color_type").set(6)
                selItem.parm("ar_format").set(2)
                selItem.parm("ar_light_color_texture").set(str(file))
                