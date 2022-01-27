# AssetBrowser
A qt asset browser for applications like houdini/nuke/maya/blender

Currently in development

Note: 
Only houdini plugin available during development

## Install
To install this tool set clone this repo into a local folder. (e.g. D:/Documents/).

### Houdini
Modify the *jsAssetBrowser.json* file that the jsAssetBrowser variable points to the plugins/houdini folder in the local clone of the repository (absolut path).
Copy the *jsAssetBrowser.json* file to the $HFS/packages folder. (e.g. D:/Documents/houdini18.0/packages)

The Asset Browser can be added as a Panel using the Python Panel Edit Tab Menu option (cogwheel top left of panel). And add the "Project Viewer (projectViewer)"-Interface to te Pane Tab Menu Entries.

## Plugins
This Module allows to add plugins for custom websites or specific file data structures/bases.

To create a plugin create a new folder for the plugin in lib/jsAssetBrowser/plugins and append the name to the plugin in plugins.json.
Note the main module file must have the same name as the folder e.g. myPlugin/myPlugin.py and needs to implement a Plugin-Class which implements the abstract PluginInterface class. (see: polyheaven as example)

In futur versions the json file will be created on runtime to manage plugins given the ability to enable or disable plugins.