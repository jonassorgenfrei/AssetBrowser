from jsAssetBrowser.api.plugin import PluginInterface

class Plugin(PluginInterface):
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