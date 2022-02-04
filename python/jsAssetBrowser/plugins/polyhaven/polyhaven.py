import json
from warnings import filters
from jsAssetBrowser.api.online_requests import request
from jsAssetBrowser.api.plugin import PluginInterface, Item

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
            filters["type"][type] = {"categorie":[]}
            categories = json.loads(request("{}/categories/{}".format(url, type)))
            for cat in categories:
              filters["type"][type]["categorie"].append(cat)              
             
        return filters
        
    def getItems(self, filters={}, search=None):
        urlAppend = ""
        
        if "type" in filters:
            urlAppend = "?t={}".format(filters["type"])
        if "categorie" in filters:
            urlAppend = "{}&c={}".format(urlAppend, filters["categorie"]) if urlAppend != "" else "?c={}".format(filters["categorie"])    
        if search is not None:
            urlAppend = "{}&s={}".format(urlAppend, search) if urlAppend != "" else "?s={}".format(search)   
             
        data = json.loads(request("{}/assets{}".format(url, urlAppend)))      
        items = [Item(self.srcKey, key, data[key]["name"], thumbs.format(KEY=key, SIZE="{SIZE}")) for key in data.keys()]
        
        return items
    
    def getCategories(self, filters={}):
        if "type" in filters:
            data = json.loads(request("{}/categories/{}".format(url, filters["type"])))      
            items = data.keys()
        else:
            itmes = []

        return items