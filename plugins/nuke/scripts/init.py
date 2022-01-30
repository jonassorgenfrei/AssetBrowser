from nukeAssetBrowser import NukeAssetBrowser
import nuke
from nukescripts import panels

# register Asset Browser Panel
if nuke.GUI:
    panels.registerWidgetAsPanel(NukeAssetBrowser.__name__, 'JS Asset Browser', 'js.AssetBrowser')
