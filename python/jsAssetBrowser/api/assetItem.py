class AssetItem():
    def __init__(self,
                 sourceKey,
                 key,
                 name,
                 prevURL,
                 tags=[],
                 previews=[]):
        self.sourceKey = sourceKey
        self.key = key
        self.name = name
        self.iconUrl = prevURL
        self.tags = tags
        self.previews = previews
        
    def getIconURL(self, size):
        return self.iconUrl.replace("{SIZE}", "{}".format(size))
       
