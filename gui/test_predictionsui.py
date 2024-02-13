from predictions import Impl_PredictionsWindow

import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

class ModelUITest(unittest.TestCase):
    def setUp(self):
        """Define initial setup"""
        self.ui = Impl_PredictionsWindow()

    def test_loadSchemaButton(self):
        """Test the Load Schema button tooltip"""
        self.assertEqual(self.ui.btn_LoadSchema.toolTip(), "Load the schema created in 'Datasets' window.")
        # Check that the Load Schema button is added and has the correct text
        btn = self.ui.btn_LoadSchema
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Load Schema")

    def test_infoSamplesBox(self):
        """Test the Samples box tooltip"""
        self.assertEqual(self.ui.txtB_InfoSamples.toolTip(), "Shows the total number of samples in the dataset.")

    def test_loadDatasetButton(self):
        """Test the Load Dataset button tooltip"""
        self.assertEqual(self.ui.btn_LoadDataset.toolTip(), "Load the dataset in csv format.")
        # Check that the Load Dataset button is added and has the correct text
        btn = self.ui.btn_LoadDataset
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Load Dataset")

    def test_loadModelButton(self):
        """Test the Load Model button tooltip"""
        self.assertEqual(self.ui.btn_LoadModel.toolTip(), "Load the model that was trained in 'Model Training' window.")
        # Check that the Load Model button is added and has the correct text
        btn = self.ui.btn_LoadModel
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Load Model")

    def test_thresholdBox(self):
        """Test the Threshold box tooltip"""
        self.assertEqual(self.ui.dsBox_Threshold.toolTip(), "Helps map a logistic regression value to binary value. Optimal value - 0.50")

    def test_HelpFeature(self):
        """Test the help feature in the window."""
        self.assertIsInstance(self.ui.btn_Help, QtWidgets.QPushButton)
        
    def test_layout(self):
        #Check the layout for the window
        self.assertIsInstance(self.ui.hlayout, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.vlayout, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.hlayout1, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout2, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout3, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout4, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout5, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.vlayout1, QtWidgets.QVBoxLayout)
    
    def test_widget_stretch(self):
        #check the stretch for the window
        self.assertEqual(self.ui.hlayout.itemAt(0).widget(), self.ui.groupBox_3)
        self.assertEqual(self.ui.hlayout.itemAt(0).widget().layout(), self.ui.hlayout1)
        self.assertEqual(self.ui.hlayout1.itemAt(0).layout(), self.ui.vlayout1)

    def test_horizontal_layout(self):
        # Check that the horizontal layout is added to the central widget
        self.assertIsInstance(self.ui.centralwidget.layout(), QtWidgets.QHBoxLayout)
    
    def test_horizontal_layout_3(self):
        #Check the horizontal layout of the window
        self.assertEqual(self.ui.hlayout3.itemAt(0).widget(), self.ui.btn_LoadSchema)
        self.assertEqual(self.ui.hlayout3.itemAt(2).widget(), self.ui.txtB_SchemaPath)

    def test_horizontal_layout_4(self):
        #Check the horizontal layout of the window
        self.assertEqual(self.ui.hlayout4.itemAt(0).widget(), self.ui.btn_LoadModel)
        self.assertEqual(self.ui.hlayout4.itemAt(2).widget(), self.ui.txtB_ModelPath)
        self.assertEqual(self.ui.hlayout4.itemAt(4).widget(), self.ui.dsBox_Threshold)

    def test_horizontal_layout_5(self):
        #Check the horizontal layout of the window
        self.assertEqual(self.ui.hlayout5.itemAt(0).widget(), self.ui.btn_Predict)
        self.assertEqual(self.ui.hlayout5.itemAt(1).widget(), self.ui.btn_SaveResults)
        self.assertEqual(self.ui.hlayout5.itemAt(2).widget(), self.ui.btn_Help)

    def test_predictButton(self):
        # Check that the Predict button is added and has the correct text
        btn = self.ui.btn_Predict
        self.assertIsInstance(btn, QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Predict")

    def test_saveButton(self):
        btn = self.ui.btn_SaveResults
        self.assertIsInstance(btn,QtWidgets.QPushButton)
        self.assertEqual(btn.text(), "Save Results")


if __name__ == "__main__":
    unittest.main()