import pymel.core as pm
       
import maya.cmds as cmds
import mayaAssetBrowser


def main():
    # this function will be executed on houdini startup!
    # Name of the global variable for the Maya window
    MainMayaWindow = pm.language.melGlobals['gMainWindow'] 
    # Build a menu and parent underthe Maya Window
    customMenu = pm.menu('JS Asset Browser', parent=MainMayaWindow)
    # Build a menu item and parent under the 'customMenu'
    pm.menuItem(label="Open Asset Browser", command=lambda arg: js_openAssetBrowser(), parent=customMenu)


def js_openAssetBrowser():
    myWindow = mayaAssetBrowser.MayaDockableAssetBrowser()
    myWindow.show(dockable=True)
    
if __name__ == "__main__":
    main()
    
# to run add:
#import sys
#sys.path.append("D:\Documents\Development\AssetBrowser\plugins\maya")
#import startUp
#startUp.main()