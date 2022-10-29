import hou

try:
    from jsAssetBrowser.api import assetBrowser
    from jsAssetBrowser.ui import assetBrowserWidget
except ModuleNotFoundError:
    # Note:
    # houdini 19.0.455 has a problem that PYTHONPATH append in the package json dosnt work
    # this is a work around by manually adding this to the python path
    import sys
    sys.path.append("{}/python".format(hou.getenv("jsAssetBrowser")))
    from jsAssetBrowser.api import assetBrowser
    from jsAssetBrowser.ui import assetBrowserWidget
    
# DEBUG
from importlib import reload

reload(assetBrowser)
reload(assetBrowserWidget)
#reload(qtUtils)
# DEBUG

"""
Module for the Houdini Asset Browser UI
"""

class HouAssetBrowser(assetBrowserWidget.AssetBrowserWidget):
    def __init__(self):
        self.assetBrowser = assetBrowser.AssetBrowser()
        super(HouAssetBrowser, self).__init__(self.assetBrowser)
        
    def asset_clicked(self):
        #super().asset_clicked()
        #caller = self.sender().parent().objectName()
        #caller = caller.replace("polyheaven.", "") 
        
        #file = super().requestFile(caller)
        #self.assign_hdr(file)
        pass
        
    def assign_hdr(self, file):
        '''
        # assign HDRI to selected item
        selItems = hou.selectedNodes()
        
        if len(selItems) > 0:
            selItem = selItems[0]
            
            nodeType = selItem.type().name()

            if nodeType in["envlight", "rslightdome::2.0"]:
                # for environment light
                selItem.parm("env_map").set(str(file))
            elif nodeType == "domelight::2.0":
                # for solaris environment light
                selItem.parm("xn__inputstexturefile_r3ah").set(str(file))
            elif nodeType == "arnold_light":
                selItem.parm("ar_light_type").set(6)
                selItem.parm("ar_light_color_type").set(6)
                selItem.parm("ar_format").set(2)
                selItem.parm("ar_light_color_texture").set(str(file))
        '''
    
    def thread_complete(self):
        #super().thread_complete()
        #print("reload texture! in Houdini")
        pass