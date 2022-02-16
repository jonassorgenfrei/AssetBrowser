import os
import nuke
from nukescripts import panels

from jsAssetBrowser.api import assetBrowser

class NukeAssetBrowser(assetBrowser.AssetBrowser):
    def __init__(self):
        super(NukeAssetBrowser, self).__init__()
    
    def asset_clicked(self):
        super().asset_clicked()
        #caller = self.sender().parent().objectName()
        #caller = caller.replace("polyheaven.", "")
        
        #file = super().requestFile(caller)

        #filePath = file.as_posix()
        #self.assign_hdr(filePath)
        
    def assign_hdr(self, filePath):
        selNodes = nuke.selectedNodes()
        
        if len(selNodes) > 0:
            selNode = selNodes[0]
            
            nodeClass = selNode.Class()
            
            if nodeClass == "Read":
                selNode.knob('file').setValue(filePath)
