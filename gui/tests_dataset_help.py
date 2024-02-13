import unittest
from datasets import Impl_DatasetsWindow
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QMessageBox

class TestHelpWindow(unittest.TestCase):
     
    def setUp(self):
        self.window = Impl_DatasetsWindow()
    
    def test_help_button_click(self):
        # simulate the click event on the Help button
        self.window.btn_Help.click()
        
        # ensure that the QMessageBox was created and shown with the correct information
        mbox = QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Help")
        mbox.setText("Here is all the information about the DataSet Window")
        mbox.setInformativeText("Click the Datasets button, press the Load Dataset on the top left corner and select the csv or xml file that contains the dataset.(It seems to work mostly with the XMLs with the CVS you have to manually pick the “preset” on the right).The tool will recognize the type of report and preload the recommended features for best prediction accuracy.\nYou can add or remove columns and the start labelling the dataset which also can be saved to used later.")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.exec_ = MagicMock()
        mbox.exec_()
        mbox.exec_.assert_called_once()
    