import json
from jsAssetBrowser.api import online_requests

class AssetItem():
    def __init__(self,
                 plugin,
                 key,
                 name,
                 prevURL,
                 tags=[],
                 previews=[],
                 assetInfoWidgetPluginWidget=None):
        self.plugin = plugin
        self.key = key
        self.name = name
        self.iconUrl = prevURL
        self.tags = tags
        self.previews = previews
        # optional a function which can append stuff to the asset info widget
        assetInfoWidgetPluginWidget = assetInfoWidgetPluginWidget
        
    def getIconURL(self, size):
        return self.iconUrl.replace("{SIZE}", "{}".format(size))
    
    def getDownloadLinks(self, resolution, ext):
        # todo change to manged by plugins individually
        hdr_json = json.loads(online_requests.request(
            "https://api.polyhaven.com/files/{}".format(self.key)))

        url = hdr_json["hdri"][resolution][ext]["url"]
        file_size = hdr_json["hdri"][resolution][ext]["size"]

        return url, file_size
    
    def getSimilarAssets(self):
        # todo change to manged by plugins individually
        similiar_json = json.loads(online_requests.request(
            "https://api.polyhaven.com/similar/{}".format(self.key)))
        
        assets = []
        for key in similiar_json:
            assets.append(self.plugin.getItem(key))
        
        return assets