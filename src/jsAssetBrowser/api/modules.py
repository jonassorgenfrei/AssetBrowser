import importlib

def loadPlugins(plugins:list=[]):
    if plugins != []:
        # create a list of plugins
        _plugins = [
            # Import the module and initialise it at the same time
            importlib.import_module(".{}".format(plugin), "jsAssetBrowser.plugins.{}".format(plugin)).Plugin() for plugin in plugins
        ]
    return _plugins