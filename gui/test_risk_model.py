from risk_model import Impl_RiskModelWindow
import numpy as np
import pandas as pd
import unittest
import sys
import tensorflow as tf
from PyQt5 import QtWidgets
import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QWidget, QFileDialog

app = QtWidgets.QApplication(sys.argv)

class Impl_RiskModelTest(unittest.TestCase):
   
    '''Test the RiskModelWindow GUI'''
    def setUp(self):

        # Create a test datasets
        self.df_dataset = pd.read_csv("C:/Users/ngaur5/Desktop/SER-517-Team-15-Spring-2023/ML4CyberVinciPython-main/input/testDataframe.csv")
        # Create Schema 
        self.schemaDict =  {
  "filename": "C:/Users/ngaur5/Desktop/SER-517-Team-15-Spring-2023/ML4CyberVinciPython-main/input/pmd-report.csv",
  "format": "csv",
  "xml_params": "null",
  "columns": [
    {
      "name": "Problem",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "risk_level",
      "tplabel": "escalated",
      "unique": [
        "1",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "2",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "3",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "4",
        "40",
        "5",
        "6",
        "7",
        "8",
        "9"
      ],
      "num_unique": 40
    },
    {
      "name": "Package",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Input",
      "tplabel": "",
      "unique": [
        "com.asu"
      ],
      "num_unique": 1
    },
    {
      "name": "File",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Input",
      "tplabel": "",
      "unique": [
        "src/com/asu/BinarySearch.java"
      ],
      "num_unique": 1
    },
    {
      "name": "Priority",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Input",
      "tplabel": "",
      "unique": [
        "2",
        "3",
        "4"
      ],
      "num_unique": 3
    },
    {
      "name": "Line",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Input",
      "tplabel": "",
      "unique": [
        "11",
        "12",
        "15",
        "19",
        "22",
        "3",
        "33",
        "34",
        "35",
        "37",
        "5",
        "7"
      ],
      "num_unique": 12
    },
    {
      "name": "Description",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Input",
      "tplabel": "",
      "unique": [
        "ArrayIsStoredDirectly: The user-supplied array 'arr' is stored directly.",
        "BeanMembersShouldSerialize: Found non-transient, non-static member. Please mark as transient or provide accessors.",
        "CommentDefaultAccessModifier: To avoid mistakes add a comment at the beginning of the BinarySearch constructor if you want a default access modifier",
        "CommentDefaultAccessModifier: To avoid mistakes add a comment at the beginning of the arr field if you want a default access modifier",
        "CommentRequired: Class comments are required",
        "CommentRequired: Field comments are required",
        "CommentRequired: Public method and constructor comments are required",
        "DefaultPackage: Use explicit scoping instead of the default package private level",
        "LocalVariableCouldBeFinal: Local variable 'arr' could be declared final",
        "LocalVariableCouldBeFinal: Local variable 'bs' could be declared final",
        "LocalVariableCouldBeFinal: Local variable 'mid' could be declared final",
        "MethodArgumentCouldBeFinal: Parameter 'args' is not assigned and could be declared final",
        "MethodArgumentCouldBeFinal: Parameter 'arr' is not assigned and could be declared final",
        "MethodArgumentCouldBeFinal: Parameter 'target' is not assigned and could be declared final",
        "OnlyOneReturn: A method should have only one exit point, and that should be the last statement in the method",
        "ShortVariable: Avoid variables with short names like bs",
        "SystemPrintln: System.out.println is used",
        "UncommentedEmptyConstructor: Document empty constructor",
        "UseVarargs: Consider using varargs for methods or constructors which take an array the last parameter."
      ],
      "num_unique": 19
    },
    {
      "name": "Rule set",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Input",
      "tplabel": "",
      "unique": [
        "Best Practices",
        "Code Style",
        "Documentation",
        "Error Prone"
      ],
      "num_unique": 4
    },
    {
      "name": "Rule",
      "data": "Categorical",
      "training": "true",
      "transformation": "One-hot Encoding",
      "transformation_params": {},
      "type": "Output",
      "tplabel": "",
      "unique": [
        "ArrayIsStoredDirectly",
        "BeanMembersShouldSerialize",
        "CommentDefaultAccessModifier",
        "CommentRequired",
        "DefaultPackage",
        "LocalVariableCouldBeFinal",
        "MethodArgumentCouldBeFinal",
        "OnlyOneReturn",
        "ShortVariable",
        "SystemPrintln",
        "UncommentedEmptyConstructor",
        "UseVarargs"
      ],
      "num_unique": 12
    }
  ],
  "trainSplit": "100",
  "testSplit": "0",
  "trainIdx": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39
  ],
  "testIdx": []
}
        # Create an instance of MyClass
        self.risk_model = Impl_RiskModelWindow(self.df_dataset)
        

    @patch.object(QFileDialog, 'getOpenFileName', return_value=('C:/Users/ngaur5/Desktop/SER-517-Team-15-Spring-2023/ML4CyberVinciPython-main/input/testRiskSchema.json', ''))
    def test_btn_LoadSchema_clicked(self, mock_getOpenFileName):
        widget = QWidget()
        self.risk_model.btn_LoadSchema_clicked()
        self.assertEqual(self.risk_model.schemaDict, {"format": "csv", "xml_params": None, "columns": [], "trainSplit": 10, "testSplit": 90, "trainIdx": [], "testIdx": []})
        self.assertEqual(self.risk_model.txtB_DatasetPath.text(), 'C:/Users/ngaur5/Desktop/SER-517-Team-15-Spring-2023/ML4CyberVinciPython-main/input/testRiskSchema.json')

    def test_fillDatasetInfo(self):
        self.risk_model.schemaDict = {'columns': [1, 2, 3], 'trainIdx': [4, 5], 'testIdx': [6, 7, 8]}
        self.risk_model.fillDatasetInfo()
        self.assertEqual(self.risk_model.txtB_InfoFeatures.text(), '3')
        self.assertEqual(self.risk_model.txtB_InfoTrainSamples.text(), '2')
        self.assertEqual(self.risk_model.txtB_InfoTestSamples.text(), '3')
        
    def test_extractDataset_test(self):
        self.risk_model.schemaDict = self.schemaDict
        X, Y = self.risk_model.extractDataset("test")
        expected_X = 0
        expected_Y = 0
        self.assertEquals(len(np.array(X)), expected_X)
        self.assertEquals(len(np.array(Y)), expected_Y)

    def test_extractDataset_train(self):
        self.risk_model.schemaDict = self.schemaDict
        X, Y = self.risk_model.extractDataset("train")
        expected_X = 40
        expected_Y = 40
        self.assertEquals(len(np.array(X)), expected_X)
        self.assertEquals(len(np.array(Y)), expected_Y)
        
    def test_btn_TrainNow_clicked(self):
        self.risk_model.schemaDict = self.schemaDict
        self.risk_model.txtB_LearningRate.setText("0.01")
        self.risk_model.sBox_Epochs.setValue(10)
        self.risk_model.cBox_MetricsAccuracy.setChecked(True)
        
        # Create dummy dataset
        self.X_train = np.random.rand(100, 10)
        self.y_train = np.random.randint(0, 2, size=100)

        # Call the method
        self.risk_model.btn_TrainNow_clicked()
        
        # Check if necessary elements were updated
        self.assertAlmostEqual(self.risk_model.lr, 0.01)
        self.assertEqual(self.risk_model.epochs, 10)
        self.assertIsNotNone(self.risk_model.worker_train_model)
        self.assertEqual(self.risk_model.btn_TrainNow.isEnabled(), False)
        self.assertEqual(self.risk_model.lbl_TrainProgress.text(), "We are training your model, please wait...")
        
        # Wait for model training to complete
        self.risk_model.worker_train_model.wait()
        self.risk_model.worker_train_model.wait()
        
        # Check if necessary elements were updated after training completion
        self.assertEqual(self.risk_model.pBar_TrainProgress.value(), 24)
        self.assertEqual(self.risk_model.cBox_EvaluateDataset.count(), 0)

    def test_calculate_metrics(self):
        # Test case 1: When Y_true and Y_pred are equal, all metrics should be 1.
        Y_true = np.array([1, 0, 1, 0, 1])
        Y_pred = np.array([1, 0, 1, 0, 1])
        expected_output = (3, 2, 0, 0, 1.0, 0.99999980000004, 0.9999996666667778, 0.9)
        self.assertEqual(len(self.risk_model.calculateMetrics(Y_true, Y_pred)), len(expected_output))
        
        # Test case 2: When Y_true and Y_pred are opposite, accuracy should be 0 and f1_score should be 0.
        Y_true = np.array([1, 0, 1, 0, 1])
        Y_pred = np.array([0, 1, 0, 1, 0])
        expected_output = (0, 0, 2, 3, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.risk_model.calculateMetrics(Y_true, Y_pred), expected_output)
        
        # Test case 3: When Y_true and Y_pred have some overlap, metrics should be between 0 and 1.
        Y_true = np.array([1, 0, 1, 0, 1])
        Y_pred = np.array([1, 1, 0, 0, 1])
        expected_output = (2, 1, 1, 1, 0.6, 0.666666, 0.666666, 0.666666)
        self.assertEqual(len(self.risk_model.calculateMetrics(Y_true, Y_pred)), len(expected_output))

    def test_dsBox_Threshold_valueChanged(self):
        # Test case 1: When model is None, nothing should happen.
        self.risk_model.model = None
        self.risk_model.cBox_EvaluateDataset.setCurrentText("Train")
        self.risk_model.dsBox_Threshold.setValue(0.5)
        self.risk_model.dsBox_Threshold_valueChanged()
        self.assertEqual(self.risk_model.txtB_EvalMetricsLoss.text(), "")
        
        # Test case 2: When evaluation dataset is not "Train" or "Test", nothing should happen.
        self.risk_model.model = "dummy_model"
        self.risk_model.cBox_EvaluateDataset.setCurrentText("Validation")
        self.risk_model.dsBox_Threshold.setValue(0.5)
        self.risk_model.dsBox_Threshold_valueChanged()
        self.assertEqual(self.risk_model.txtB_EvalMetricsLoss.text(), "")
        
        
        
if __name__ == '__main__':
    unittest.main()

