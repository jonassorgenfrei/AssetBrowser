bl_info = {
     # required
    "name": "JS Asset Browser",
    "blender": (2, 90, 0),
    "category": "Object",
    # optional
    "author": "Jonas Sorgenfrei",
    "version": (1, 4, 4),
    "location": "View3D > JS Asset Browser",
    "description": "Asset Browser",
    "doc_url": "https://github.com/jonassorgenfrei/AssetBrowser",
    "tracker_url": "https://github.com/jonassorgenfrei/AssetBrowser/issues",
}

import bpy

from . import bAssetBrowser

CLASSES = [
    bAssetBrowser.BlendAssetBrowser,
]

def register():
    print('registered') # just for debug
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    print('unregistered') # just for debug
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()