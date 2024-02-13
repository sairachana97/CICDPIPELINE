from datasets_labeler import Impl_DatasetsLabelerWindow

import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

app = QApplication(sys.argv)

class DatasetLabelerUITest(unittest.TestCase):
    def setUp(self):
        """Define initial setup"""
        self.ui = Impl_DatasetsLabelerWindow("")

    def test_sizeBox(self):
        """Test the Size box tooltip"""
        self.assertEqual(self.ui.sBox_SampleSize.toolTip(), "Sets the size of the data for training.")
        
    def test_sizePercentageBox(self):
        """Test the Size(%) box tooltip"""
        self.assertEqual(self.ui.dsBox_SamplePerc.toolTip(), "Sets the percentage of the sampling data for training.")

    def test_typeBox(self):
        """Test the Type box tooltip"""
        self.assertEqual(self.ui.cBox_SampleType.toolTip(), "Choose the type of sampling to be performed.")

    def test_customSeedBox(self):
        """Test the Custom Seed box tooltip"""
        self.assertEqual(self.ui.sBox_CustomSeed.toolTip(), "Allows user to add seed values so that the results are similar each time.")

    def test_invertSampleBox(self):
        """Test the Invert Sample checkbox tooltip"""
        self.assertEqual(self.ui.chkBox_InvertSample.toolTip(), "Allows to generate samples at random.")

    def test_trueLabelBox(self):
        """Test the True Label box tooltip"""
        self.assertEqual(self.ui.txtB_TrueLabel.toolTip(), "The value to be assigned for true samples.")

    def test_falseLabelBox(self):
        """Test the False Label box tooltip"""
        self.assertEqual(self.ui.txtB_FalseLabel.toolTip(), "The value to be assigned for false samples.")

    def test_columnLabelBox(self):
        """Test the Column Label box tooltip"""
        self.assertEqual(self.ui.txtB_ColumnLabel.toolTip(), "Name of the output column.")

    def test_allHorizontalLayout(self):
        self.assertIsInstance(self.ui.hlayout, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout1, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout12, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout13, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout21, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout3, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout31, QtWidgets.QHBoxLayout)

    def test_allVerticalLayout(self):
        self.assertIsInstance(self.ui.vlayout, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.group_vlayout1, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.group_vlayout2, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.group_vlayout321, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.group_vlayout31, QtWidgets.QVBoxLayout)

    def test_allChildLayouts(self):
        self.assertIsInstance(self.ui.hlayout, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout1, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.group_hlayout1.itemAt(0), QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.group_vlayout1.itemAt(0), QtWidgets.QHBoxLayout)


if __name__ == "__main__":
    unittest.main()