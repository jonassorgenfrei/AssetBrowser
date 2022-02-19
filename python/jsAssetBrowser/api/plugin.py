# An Interface for Plugins

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

    def getCategories(self, filters={}):
        """Returns a list of categories
        """
        pass
    
    def getPreviews(self):
        pass
