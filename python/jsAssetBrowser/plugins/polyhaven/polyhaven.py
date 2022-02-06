import json
from warnings import filters
from jsAssetBrowser.api.online_requests import request
from jsAssetBrowser.api.plugin import PluginInterface
from jsAssetBrowser.api.assetItem import AssetItem

# poly haven HDRI api
url = "https://api.polyhaven.com"
thumbs = "https://cdn.polyhaven.com/asset_img/thumbs/{KEY}.png?height={SIZE}"

class Plugin(PluginInterface):
    srcKey = "polyheaven"
    
    def __init__(self):
        super().__init__()
        print("Polyhaven")

    def run(self):
        """
        """
        pass

    def help(self):
        print("Help for Polyhaven-Plugin.")
        print("- Queries assets and data from: https://polyhaven.com/")

    def getFilters(self):
        types = json.loads(request("{}/types".format(url)))
        
        filters = {"type": {}}
        
        for type in types:
            filters["type"][type] = {"category":[]}
            categories = json.loads(request("{}/categories/{}".format(url, type)))
            for cat in categories:
              filters["type"][type]["category"].append(cat)              
             
        return filters
        
    def getItems(self, filters={}, search=None):
        urlAppend = ""
        
        if "type" in filters:
            urlAppend = "?t={}".format(filters["type"])
        if "category" in filters:
            urlAppend = "{}&c={}".format(urlAppend, filters["category"]) if urlAppend != "" else "?c={}".format(filters["category"])    
        if search is not None:
            urlAppend = "{}&s={}".format(urlAppend, search) if urlAppend != "" else "?s={}".format(search)   
        urlAppend = urlAppend.replace(" ", "%20")
        data = json.loads(request("{}/assets{}".format(url, urlAppend)))      
        items = [AssetItem(self.srcKey, key, data[key]["name"], thumbs.format(KEY=key, SIZE="{SIZE}")) for key in data.keys()]
        
        return items
    
    def getCategories(self, filters={}):
        if "type" in filters:
            data = json.loads(request("{}/categories/{}".format(url, filters["type"])))      
            items = data.keys()
        else:
            itmes = []

        return items