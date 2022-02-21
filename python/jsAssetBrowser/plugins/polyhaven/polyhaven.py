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
        """ """
        pass

    def help(self):
        print("Help for Polyhaven-Plugin.")
        print("- Queries assets and data from: https://polyhaven.com/")

    def getFilters(self):
        types = json.loads(request("{}/types".format(url)))

        filters = {"type": {}}

        for type in types:
            filters["type"][type] = {"category": []}
            categories = json.loads(request("{}/categories/{}".format(url, type)))
            for cat in categories:
                filters["type"][type]["category"].append(cat)

        return filters

    def getItems(self, filters={}, search=None):
        urlAppend = ""

        if "type" in filters:
            urlAppend = "?t={}".format(filters["type"])
        if "category" in filters:
            urlAppend = (
                "{}&c={}".format(urlAppend, filters["category"])
                if urlAppend != ""
                else "?c={}".format(filters["category"])
            )
        if search is not None:
            urlAppend = (
                "{}&s={}".format(urlAppend, search)
                if urlAppend != ""
                else "?s={}".format(search)
            )
        urlAppend = urlAppend.replace(" ", "%20")
        data = json.loads(request("{}/assets{}".format(url, urlAppend)))
        
        items = []
        for key in data.keys():
            
            if data[key]["type"] == 0:  # HDRIS
                previews =  [
                    "https://cdn.polyhaven.com/asset_img/thumbs/{}.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/primary/{}.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/renders/{}/lone_monk.png?height=246&height=413".format(key)
                ]
            elif data[key]["type"] == 1: # textures
                previews = [
                    "https://cdn.polyhaven.com/asset_img/thumbs/{}.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/primary/{}.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/renders/{}/clay.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_ao_1k.jpg?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_arm_1k.jpg?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_diff_1k.jpg?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_disp_1k.jpg?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_nor_gl_1k.jpg?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_rough_1k.jpg?height=246&height=413".format(key)
                ]
            elif data[key]["type"] == 2: # models
                previews = [
                    "https://cdn.polyhaven.com/asset_img/primary/{}.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/renders/{}/clay.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/renders/{}/orth_front.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/renders/{}/orth_side.png?height=246&height=413".format(key),
                    "https://cdn.polyhaven.com/asset_img/renders/{}/orth_top.png?height=246&height=413".format(key)                  
                ]
                
                # TODO implement delayed loading of model preview file links
                #fileData = json.loads(request("{}/files/{}".format(url, key)))
                #for file in fileData.keys():
                #    if file != "fbx" and file != "gltf" and file != "blend":
                #        prevFile = "https://cdn.polyhaven.com/asset_img/map_previews/{0}/{0}_{1}_1k.jpg?height=246&height=413".format(key, file)
                #        previews.append(prevFile)
            
            item = AssetItem(
                self.srcKey,
                key,
                data[key]["name"],
                thumbs.format(KEY=key, SIZE="{SIZE}"),
                data[key]["tags"],
                previews,
            )
            items.append(item)

        return items

    def getCategories(self, filters={}):
        if "type" in filters:
            data = json.loads(request("{}/categories/{}".format(url, filters["type"])))
            items = data.keys()
        else:
            itmes = []

        return items