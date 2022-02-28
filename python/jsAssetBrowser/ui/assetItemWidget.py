import os

from jsAssetBrowser.ui import fontAwesome_icons_rc
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

font_path = os.path.join(os.path.dirname(__file__), "external", "fonts", "OpenSansCondensed-Bold.ttf")
_id = QtGui.QFontDatabase.addApplicationFont(font_path)

class AssetItemButton(QtWidgets.QToolButton):
    mouseHover = QtCore.Signal(bool)
    
    def __init__(self, parent):
        super(AssetItemButton, self).__init__(parent)
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        self.mouseHover.emit(True)
        
    def leaveEvent(self, event):
        self.mouseHover.emit(False)

class AssetItemWidget(QtWidgets.QWidget):
    def __init__(self,
                 thumbsize,
                 assetItem,
                 cached_assets):
        super(AssetItemWidget, self).__init__()
        
        # item data 
        self.assetItem = assetItem
        self.thumbsize = thumbsize
        self.label = self.assetItem.name

        self.cached_assets = cached_assets
        self.key = self.assetItem.key
        self.setMinimumSize(thumbsize)
        
        self.setToolTip(self.label)
        
        # main button image
        self.btn = AssetItemButton(self)
        self.btn.setFixedSize(thumbsize)
        self.btn.setIconSize(thumbsize)
        self.btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.btn.setStyleSheet("QToolButton{background: #3d3d3d}"\
                               "QToolButton::hover{background:#3d3d3d; border: 3px solid #ffffff;}")
        
        # corner button 
        self.cornerBtn = QtWidgets.QPushButton(self)
        self.cornerBtn.setIcon(QtGui.QIcon(":/font-awesome/external/fontAwesome/svgs/solid/check-circle.svg"))
        self.cornerBtn.setProperty('transparent', True)
        self.cornerBtn.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.lbl_name_size = thumbsize.height()/16
        
        self.cornerBtn.resize(50,50)
        self.cornerBtn.move(thumbsize.width()-60,10)

        self.name_lbl = QtWidgets.QLabel(self.label, self)
        self.name_lbl.move(5, int(thumbsize.height()/1.5)-self.name_lbl.sizeHint().height())
        self.name_lbl.hide()
        self.name_lbl.setStyleSheet("QLabel{font-family: " + QtGui.QFontDatabase.applicationFontFamilies(_id)[0] + ";"\
                                    "font-size: " + str(self.lbl_name_size)+ ";"\
                                    "color:#ffffff;"\
                                    "background-color: #88000000;}")
        self.name_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.btn.mouseHover.connect(self.name_lbl.setVisible)
        
    def setIcon(self, image):
        self.btn.setIcon(image)
        
    def setIconFromData(self):
        imgBlob = self.cached_assets[self.key]
        qImg = QtGui.QImage.fromData(imgBlob)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.setIcon(QtGui.QIcon(pixmap))
        