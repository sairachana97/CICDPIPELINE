import unittest
from models import Impl_ModelsWindow
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QMessageBox

class TestHelpWindow(unittest.TestCase):
     
    def setUp(self):
        self.window = Impl_ModelsWindow()
    
    def test_help_button_click(self):
        # simulate the click event on the Help button
        self.window.btn_Help.click()
        
        # ensure that the QMessageBox was created and shown with the correct information
        mbox = QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Help")
        mbox.setText("Here is all the information about the Model Window")
        mbox.setInformativeText("Load the schema you created and press “Train Now”, select a high Epochs number for higher accuracy. At the lower half of this page you can select to view the Test set (Dataset Sample drop box) accuracy and metrics also if the whole dataset is labeled. See how changing the threshold the values are affected also. Save the model by pressing Save Model on the middle right. Save it by adding the .h5 extension.")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.exec_ = MagicMock()
        mbox.exec_()
        mbox.exec_.assert_called_once()
    