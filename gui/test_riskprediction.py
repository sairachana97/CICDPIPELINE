import unittest
from unittest.mock import patch, MagicMock
from risk_predictions import Impl_RiskPredictionsWindow
from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import sys
import tensorflow as tf

app = QtWidgets.QApplication(sys.argv)

class RiskPredictionUITest(unittest.TestCase):

    def setUp(self):
        self.riskpredictionwindow = Impl_RiskPredictionsWindow()
        self.widget = MagicMock()
        self.file_name = "model.h5"
        self.options = QtWidgets.QFileDialog.Options()
        self.options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.file_filter = "H5 Files (*.h5)"

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', val = ('ML4CyberVinciPython-main/input/testRiskDataset.csv', ''))
    def test_btn_LoadDataset_clicked(self, mock_file):
        riskpredictionwindow = Impl_RiskPredictionsWindow()
        riskpredictionwindow.txtB_DatasetPath - MagicMock()
        riskpredictionwindow.btn_LoadDataset_clicked()
        mock_file.assert_called_once_with(
            riskpredictionwindow,
            "Open Dataset File",
            "",
            "CSV Files (*.csv)",
            options = QtWidgets.QFileDialog.Options() | QtWidgets.QFileDialog.DontUseNativeDialog
        )
        riskpredictionwindow.txtB_DatasetPath.setText.assert_called_once_with('ML4CyberVinciPython-main/input/testRiskDataset.csv')

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_btn_LoadSchema_clicked(self, mock_file_dialog):
        mock_file_dialog.return_value = ('input/test_schema.json', '')
        self.riskpredictionwindow.btn_LoadSchema_clicked()
        # Create a MagicMock object to represent the function
        self.riskpredictionwindow.checkFilesHealth = MagicMock()
        self.riskpredictionwindow.loadDataframe = MagicMock()

        # Call the function
        self.riskpredictionwindow.checkFilesHealth()
        self.riskpredictionwindow.loadDataframe()

        self.assertEqual(self.riskpredictionwindow.schemaDict["format"], "csv")
        self.assertEqual(self.riskpredictionwindow.txtB_SchemaPath.text(), 'input/test_schema.json')
        self.assertTrue(self.riskpredictionwindow.checkFilesHealth.called)
        self.assertTrue(self.riskpredictionwindow.loadDataframe.called)

    @patch("tf.keras.models.load_model")
    def test_loadModel(self, mock_load_model):
        self.txtB_ModelPath = MagicMock()
        mock_load_model.return_value = "mock model"
        self.riskpredictionwindow.btn_LoadModel_clicked(self)
        self.assertEqual(self.model, "mock model")
        self.assertEqual(self.txtB_ModelPath.setText.call_args[0][0], self.file_name)

    def test_Predict(self):
        self.riskpredictionwindow.btn_Predict_clicked()
        self.assertIsNotNone(self.riskpredictionwindow.preds)
        self.assertTrue(self.riskpredictionwindow.btn_SaveResults.isEnabled())

    @patch('builtins.QFileDialog.getSaveFileName', return_value=('test.csv', 'CSV Files (*.csv)'))
    @patch('pandas.DataFrame.to_csv')
    @patch('PyQt5.QtWidgets.QMessageBox.exec_')
    def test_saveResults(self, mock_exec, mock_to_csv, mock_getSaveFileName):
        self.riskpredictionwindow.btn_SaveResults_clicked()
        mock_getSaveFileName.assert_called_once_with(self.riskpredictionwindow, 'Save Results File', '', 'CSV Files (*.csv)', options=2)
        mock_to_csv.assert_called_once_with('test.csv')
        mock_exec.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
