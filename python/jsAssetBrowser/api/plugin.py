# An Interface for Plugins

class PluginInterface():
    srcKey = "PLUGIN_INTERFACE"
    def __init__(self):
        print("Loaded Plugin: ", end='')
    
    def run(self):
        raise NotImplementedError

    def help(self):
        raise NotImplementedError
    
    def getFilter(self):
        raise NotImplementedError
    
    def getItems(self, filters={}, search=None):
        """Returns a list of items
        """
        raise NotImplementedError

    def getItem(self, key):
        """Returns the requestes item
        """
        raise NotImplementedError

    def getCategories(self, filters={}):
        """Returns a list of categories
        """
        raise NotImplementedError
    
    def getPreviews(self):
        raise NotImplementedError
