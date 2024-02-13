import unittest
from predictions import Impl_PredictionsWindow
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QMessageBox

class TestHelpWindow(unittest.TestCase):
     
    def setUp(self):
        self.window = Impl_PredictionsWindow()
    
    def test_help_button_click(self):
        # simulate the click event on the Help button
        self.window.btn_Help.click()
        
        # ensure that the QMessageBox was created and shown with the correct information
        mbox = QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Help")
        mbox.setText("Here is all the information about the Predictions Window")
        mbox.setInformativeText("Load the original dataset, the schema you created and the training model. Press Predict and Save Results when finished to save a .csv file with the predictions.")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.exec_ = MagicMock()
        mbox.exec_()
        mbox.exec_.assert_called_once()
    