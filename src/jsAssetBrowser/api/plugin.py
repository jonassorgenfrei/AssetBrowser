# An Interface for Plugins

class PluginInterface():
    def __init__(self):
        print("Loaded Plugin: ", end='')
    
    def run(self):
        pass

    def help(self):
        pass
