from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

from menu_ui import Ui_MainWindow
from datasets import Impl_DatasetsWindow
from models import Impl_ModelsWindow
from predictions import Impl_PredictionsWindow
from help import Impl_HelpWindow
from risk import Impl_RiskWindow


class Impl_MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    """Creates menu window"""

    def __init__(self):
        """Initializes menu window object"""
        super(Impl_MainWindow, self).__init__()
        self.setupUi(self)

        self.customEvents()
        self.customInit()

    def customInit(self):
        """Custom init method"""
        pass

    def customEvents(self):
        """Custom events method; here you connect functions with the UI."""
        self.btn_Datasets.clicked.connect(self.btn_Datasets_clicked)
        self.btn_Models.clicked.connect(self.btn_Models_clicked)
        # 2023 september (sprint 2)
        self.btn_Risk.clicked.connect(self.btn_Risk_clicked)
        self.btn_Risk.setGeometry(100, 100, 400, 300)
        self.risk_window = None

        self.btn_Predictions.clicked.connect(self.btn_Predictions_clicked)
        self.btn_Help.clicked.connect(self.btn_Help_clicked)

    def btn_Datasets_clicked(self):
        """Clicked event on btn_Datasets component.
        Loads and shows Datasets Window.
        """
        self.ds_ui = Impl_DatasetsWindow()
        self.ds_ui.show()
        self.close()

    def btn_Models_clicked(self):
        """Clicked event on btn_Models component.
        Loads and shows Models Window.
        """
        self.md_ui = Impl_ModelsWindow()
        self.md_ui.show()

        self.close()


    def btn_Predictions_clicked(self):
        """Clicked event on btn_Preditions component.
        Loads and shows Predictions Window.
        """
        self.pd_ui = Impl_PredictionsWindow()
        #self.pd_ui.window_closed.connect(self.reloadScreen)
        self.pd_ui.show()
        self.close()
        

    # 2023 September (sprint2)
    def btn_Risk_clicked(self):
        self.risk_window = Impl_RiskWindow()
        #self.risk_window.window_closed.connect(self.reloadScreen)
        self.risk_window.show()
        self.close()

    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
        Loads and show Help Window.
        """

        self.hs_ui = Impl_HelpWindow("Main")
        self.hs_ui.show()
        