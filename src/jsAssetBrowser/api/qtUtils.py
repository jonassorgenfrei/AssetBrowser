from PySide2 import QtGui, QtCore

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
        