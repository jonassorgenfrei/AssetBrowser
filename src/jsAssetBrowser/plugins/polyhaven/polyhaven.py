import json
from jsAssetBrowser.api.online_requests import request
from jsAssetBrowser.api.plugin import PluginInterface

# poly haven HDRI api
url = "https://api.polyhaven.com/assets?t=hdris"


class Plugin(PluginInterface):
    def __init__(self):
        super().__init__()
        print("Polyhaven")

    def run(self):
        """
        """
        data = json.loads(request(url))
        print(data)

    def help(self):
        print("Help for Polyhaven-Plugin.")
        print("- Queries assets and data from: https://polyhaven.com/")
