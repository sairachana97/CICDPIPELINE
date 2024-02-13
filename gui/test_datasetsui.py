from datasets import Impl_DatasetsWindow

import sys
import unittest
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

class DatasetUITest(unittest.TestCase):
    def setUp(self):
        """Define initial setup"""
        self.ui = Impl_DatasetsWindow()

    def test_columnBox(self):
        """Test the Column box tooltip"""
        self.assertEqual(self.ui.cBox_Column.toolTip(), "Displays a dropdown of the columns present in the dataset.")
        
    def test_transformationBox(self):
        """Test the Transformation box tooltip"""
        self.assertEqual(self.ui.cBox_Transformation.toolTip(), "Converts label values to binary values.")

    def test_dataBox(self):
        """Test the Data box tooltip"""
        self.assertEqual(self.ui.cBox_Data.toolTip(), "Type of the data - Categorical(label values) or Numerical.")

    def test_typeBox(self):
        """Test the Type box tooltip"""
        self.assertEqual(self.ui.cBox_Type.toolTip(), "Type of the data - Input or Output.")

    def test_TPLabelBox(self):
        """Test the TPLabel box tooltip"""
        self.assertEqual(self.ui.cBox_TPLabel.toolTip(), "Displays the available labels for the selected column.")

    def test_rootBox(self):
        """Test the Root box tooltip"""
        self.assertEqual(self.ui.cBox_Root.toolTip(), "It depicts the hierarchy of XML tags.")

    def test_trainingBox(self):
        """Test the Training box tooltip"""
        self.assertEqual(self.ui.cBox_Training.toolTip(), "It shows if the data has been trained or not.")

    def test_presetBox(self):
        """Test the Preset box tooltip"""
        self.assertEqual(self.ui.cBox_Preset.toolTip(), "List of static code analyser tools and corresponding report formats.")

if __name__ == "__main__":
    unittest.main()