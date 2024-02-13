import unittest
from PyQt5 import QtWidgets
from menu import Impl_MainWindow

class TestImplPredictionsWindow(unittest.TestCase):
    
    def setUp(self):
        self.window = Impl_MainWindow()
    
    def test_layout(self):
        #Check the layout for the window
        self.assertIsInstance(self.window.hlayout, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.window.vlayout, QtWidgets.QVBoxLayout)

    def test_button_Dataset(self):
        # Check that the Load Dataset button is added and has the correct text
        btn = self.window.btn_Datasets
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Datasets")

    def test_button_Models(self):
        # Check that the Load Schema button is added and has the correct text
        btn = self.window.btn_Models
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Model Training")

    def test_predict_button(self):
        # Check that the Predict button is added and has the correct text
        btn = self.window.btn_Predictions
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Predictions")

    def test_save_button(self):
        btn = self.window.btn_Help
        self.assertIsInstance(btn,QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Help")

if __name__ == '__main__':
    unittest.main()
