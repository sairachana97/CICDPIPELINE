from help_ui import Ui_HelpWindow
from PyQt5 import QtCore, QtWidgets


class Impl_HelpWindow(Ui_HelpWindow, QtWidgets.QMainWindow):
    """Creates predictions window"""
    

    def __init__(self, type):
        """Initializes help window object"""
        super(Impl_HelpWindow, self).__init__()
        self.type = type
        self.setupUi(self)
        self.customInit()


    def customInit(self):
        """Custom init method"""
        self.df_dataset = None
        self.schemaDict = None
        self.model = None
        self.tp_label = None
        self.preds = None
        self.bin_preds = None