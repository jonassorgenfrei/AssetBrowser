from PySide2 import QtWidgets, QtGui, QtNetwork, QtCore, QtUiTools

class AssetBrowserWidget(QtWidgets.QWidget):
    """The main Ui for the asset browser

    Args:
        QtWidgets (_type_): _description_
    """
    def __init__(self):
        super(AssetBrowserWidget, self).__init__()
        