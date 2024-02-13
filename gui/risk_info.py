from PyQt5 import QtCore, QtWidgets
from risk_info_ui import Ui_RiskInfoWindow


class Impl_RiskInfoWindow(Ui_RiskInfoWindow, QtWidgets.QMainWindow):
    """Creates risk info window"""

    def __init__(self):
        """Initializes risk window object"""
        super(Ui_RiskInfoWindow, self).__init__()
        self.setupUi(self)

        self.customInit()
        self.customEvents()

    def customInit(self):
        """Custom init method"""
        self.setWindowModality(QtCore.Qt.WindowModal)

    def customEvents(self):
        """Custom events method; here you connect functions with the UI."""
        pass
