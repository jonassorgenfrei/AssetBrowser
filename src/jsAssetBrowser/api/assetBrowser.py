import os
import json

from PySide2 import QtWidgets, QtUiTools

from jsAssetBrowser.api import modules

# DEBUG
from importlib import reload
reload(modules)
# DEBUG

dirname = os.path.dirname(__file__)


class AssetBrowser(QtWidgets.QWidget):
    def __init__(self):
        super(AssetBrowser, self).__init__()

        #print("Init Asset Browser")
        #print("Loading Modules/Plugins")

        with open('{}/../plugins/plugins.json'.format(dirname), 'r') as f:
            pluginsNames = json.load(f)

        plugins = modules.loadPlugins(pluginsNames["plugins"])

        for plugin in plugins:
            plugin.run()

        #print("Finished Plugin Loading")
