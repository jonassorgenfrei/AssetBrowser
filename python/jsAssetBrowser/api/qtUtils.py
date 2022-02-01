from PySide2 import QtGui, QtCore
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
        self.set_widget_image(the_reply)
        
    def set_widget_image(self, img_binary):
        self.pixmap.loadFromData(img_binary)
        icon = QtGui.QIcon()
        icon.addPixmap(self.pixmap)        
        self.parent().setIcon(icon)

class WorkerSignal(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int)
    
class Worker(QtCore.QRunnable):
    # Worker thread
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
        
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