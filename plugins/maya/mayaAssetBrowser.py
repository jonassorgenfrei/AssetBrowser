# note: https://kainev.com/qt-for-maya-dockable-windows/
import os
try:
    from jsAssetBrowser.api import assetBrowser
except ModuleNotFoundError:
    # Note:
    # houdini 19.0.455 has a problem that PYTHONPATH append in the package json dosnt work
    # this is a work around by manually adding this to the python path
    import sys
    sys.path.append("{}/python".format(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    from jsAssetBrowser.api import assetBrowser
    
    
from jsAssetBrowser.api import assetBrowser

from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui

class MayaAssetBrowser(assetBrowser.AssetBrowser):
    def __init__(self):
        super(MayaAssetBrowser, self).__init__()

'''
class DockableBase(MayaQWidgetDockableMixin):
    """
    Convenience class for creating dockable Maya windows.
    """
    def __init__(self, controlName, **kwargs):
        super(DockableBase, self).__init__(**kwargs)
        self.setObjectName(controlName)   
                                    
    def show(self, *args, **kwargs):
        """
        Show UI with generated uiScript argument
        """
        modulePath = inspect.getmodule(self).__name__
        className = self.__class__.__name__
        super(DockableBase, self).show(dockable=True,
                                        uiScript="import {0}; {0}.{1}._restoreUI()".format(modulePath, className), **kwargs)
        
    @classmethod
    def _restoreUI(cls):
        """
        Internal method to restore the UI when Maya is opened.
        """
        # Create UI instance
        instance = cls()
        # Get the empty WorkspaceControl created by Maya
        workspaceControl = omui.MQtUtil.getCurrentParent()
        # Grab the pointer to our instance as a Maya object
        mixinPtr = omui.MQtUtil.findControl(instance.objectName())
        # Add our UI to the WorkspaceControl
        omui.MQtUtil.addWidgetToMayaLayout(long(mixinPtr), long(workspaceControl))
        # Store reference to UI
        global mixinWindows
        mixinWindows[instance.objectName()] = instance		
'''

class MayaDockableAssetBrowser(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MayaDockableAssetBrowser, self).__init__(parent=parent)
        
        self.setObjectName("jsAssetBrowser")
        self.setWindowTitle("JS Asset Browser")
        
        self.assetBrowser = MayaAssetBrowser()
        
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.assetBrowser)
        
        self.setLayout(mainLayout)
        
        
'''
For adding it as a plugin!


import sys
import maya.api.OpenMaya as om

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass


# command
class PyHelloWorldCmd(om.MPxCommand):
	kPluginCmdName = "pyHelloWorld"

	def __init__(self):
		om.MPxCommand.__init__(self)

	@staticmethod
	def cmdCreator():
		return PyHelloWorldCmd()

	def doIt(self, args):
		print "Hello World!"


# Initialize the plug-in
def initializePlugin(plugin):
	pluginFn = om.MFnPlugin(plugin)
	try:
		pluginFn.registerCommand(
			PyHelloWorldCmd.kPluginCmdName, PyHelloWorldCmd.cmdCreator
		)
	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % PyHelloWorldCmd.kPluginCmdName
		)
		raise


# Uninitialize the plug-in
def uninitializePlugin(plugin):
	pluginFn = om.MFnPlugin(plugin)
	try:
		pluginFn.deregisterCommand(PyHelloWorldCmd.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % PyHelloWorldCmd.kPluginCmdName
		)
		raise
'''
