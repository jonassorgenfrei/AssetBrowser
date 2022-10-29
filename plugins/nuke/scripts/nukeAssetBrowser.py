import os
import nuke
from nukescripts import panels
from PySide2.QtWidgets import QWidget

try:
    from jsAssetBrowser.api import assetBrowser
    from jsAssetBrowser.ui import assetBrowserWidget
except Exception as e:
    print(e)
    
class NukeAssetBrowser(assetBrowserWidget.AssetBrowserWidget):
    def __init__(self):
        self.assetBrowser = assetBrowser.AssetBrowser()
        super(NukeAssetBrowser, self).__init__(self.assetBrowser)
    
    def asset_clicked(self):
        super().asset_clicked()
        #caller = self.sender().parent().objectName()
        #caller = caller.replace("polyheaven.", "")
        
        #file = super().requestFile(caller)

        #filePath = file.as_posix()
        #self.assign_hdr(filePath)
        
    def assign_hdr(self, filePath):
        pass
        #selNodes = nuke.selectedNodes()
        
        #if len(selNodes) > 0:
        #    selNode = selNodes[0]
            
        #    nodeClass = selNode.Class()
            
        #    if nodeClass == "Read":
        #        selNode.knob('file').setValue(filePath)
