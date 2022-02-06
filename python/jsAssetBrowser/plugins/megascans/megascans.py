import json
from warnings import filters
from jsAssetBrowser.api.online_requests import request
from jsAssetBrowser.api.plugin import PluginInterface, Item

# megascan url

class Plugin(PluginInterface):
    srcKey = "quixel"
    
    def __init__(self):
        super().__init__()
        print("Quixel Megascan")

    def run(self):
        """
        """
        pass

    def help(self):
        print("Help for Quixel Megascan-Plugin.")
        print("- Queries assets and data from: https://quixel.com/megascans/")

    def getFilters(self):
        pass
        
    def getItems(self, filters={}, search=None):
        pass
    
    def getCategories(self, filters={}):
        pass