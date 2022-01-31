from jsAssetBrowser.api.plugin import PluginInterface

# check implementation: https://github.com/sketchfab/blender-plugin
class Plugin(PluginInterface):
    srcKey = "sketchfab"
    
    def __init__(self):
        super().__init__()
        print("Sketchfab")

    def run(self):
        """
        """
        pass

    def help(self):
        print("Help for Sketchfab-Plugin.")
        print("- Queries assets and data from: https://sketchfab.com")
    
    def getItems(self):
        pass