# An Interface for Plugins

class Item():
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

class PluginInterface():
    def __init__(self):
        print("Loaded Plugin: ", end='')
    
    def run(self):
        pass

    def help(self):
        pass
    
    def getFilter(self):
        pass
    
    def getItems(self, filters={}, search=None):
        """Returns a list of items
        """
        pass
