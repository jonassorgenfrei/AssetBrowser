class AssetItem():
    def __init__(self,
                 sourceKey,
                 key,
                 name,
                 prevURL):
        self.sourceKey = sourceKey
        self.key = key
        self.name = name
        self.iconUrl = prevURL
        
    def getIconURL(self, size):
        return self.iconUrl.replace("{SIZE}", "{}".format(size))
       
