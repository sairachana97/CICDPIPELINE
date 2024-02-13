import unittest
from datasets import Impl_DatasetsLabelerWindow
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QMessageBox

class TestHelpWindow(unittest.TestCase):
     
    def setUp(self):
        self.window = Impl_DatasetsLabelerWindow()
    
    def test_help_button_click(self):
        # simulate the click event on the Help button
        self.window.btn_Help.click()
        
        # ensure that the QMessageBox was created and shown with the correct information
        mbox = QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Help")
        mbox.setText("Here is all the information about the Labeler Window")
        mbox.setInformativeText("You can separate here the training set. Load the dataset you saved as a .csv file before, select the Stratified type and save the training set.\nLoad the training dataset you just created at the Dataset Labeling section. Each finding will be displayed separately and you will be able to assign the True or False label using the check boxes on the right. Save the dataset and close the window.")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.exec_ = MagicMock()
        mbox.exec_()
        mbox.exec_.assert_called_once()
    