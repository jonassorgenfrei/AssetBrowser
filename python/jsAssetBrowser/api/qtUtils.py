from jsAssetBrowser.api import config, database
from jsAssetBrowser.ui import assetItemWidget
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Slot

import sys
import traceback

class ImgDownloader(QtCore.QObject):
    def __init__(self, parent, req):
        self.req = req
        self.pixmap = QtGui.QPixmap()
        super(ImgDownloader, self).__init__(parent)
    
    def start_fetch(self, net_mgr):
        self.fetch_task = net_mgr.get(self.req)
        self.fetch_task.finished.connect(self.resolve_fetch)
        
    def resolve_fetch(self):
        the_reply = self.fetch_task.readAll()
        if isinstance(self.parent(), assetItemWidget.AssetItemWidget):
            self.set_widget_image(the_reply)
        elif isinstance(self.parent(), QtWidgets.QLabel):
            self.set_lbl_img(the_reply)
            
        
    def set_widget_image(self, img_binary):
        self.pixmap.loadFromData(img_binary)
        icon = QtGui.QIcon()
        icon.addPixmap(self.pixmap)        
        self.parent().setIcon(icon)
        
        db = database.Database(config.Config())
        db.insertImg(self.parent().key, 
                     self.parent().thumbsize.height(), 
                     img_binary)

    def set_lbl_img(self, img_binary):
        self.pixmap.loadFromData(img_binary)    
        self.parent().setPixmap(self.pixmap)
        
        #db = database.Database(config.Config())
        #db.insertImg(self.parent().key, 
        #             self.parent().thumbsize.height(), 
        #             img_binary)

class AssetBrowserWorkerSignal(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int)
    
class AssetBrowserWorker(QtCore.QRunnable):
    # Worker thread
    def __init__(self, fn, *args, **kwargs):
        super(AssetBrowserWorker, self).__init__()
        
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = AssetBrowserWorkerSignal()
        
        # signal to kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        
    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, 
                                     value, 
                                     traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
            
    # alternative
    #for i in reversed(range(self.ui.categories.count())): 
    #        self.ui.categories.itemAt(i).widget().setParent(None)
