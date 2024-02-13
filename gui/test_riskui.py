from risk_from_labeller import Impl_RiskWindow_from_Labeller

import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
import pandas as pd
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

class RiskUITest(unittest.TestCase):
    
    def setUp(self):
        """Define initial setup"""
        data = {'@status': ['escalated', 'escalated', 'escalated', 'escalated'],
    '@severity': ['info', 'info', 'info', 'info'],
    'cwe->@id': [1,2,3,4],
    'results->result->description->#text': ['wfeqwf', 'ewfqwf', 'qwfd', 'qef'],
    'results->result->tool->@category': ['wegv', 'wefv', 'sfdv', 'dv'],
    'results->result->tool->@name': ['ace', 'ber', 'wqef', 'vbsd'],
    'rule->@code': ['wfegv', 'qqw', 'hyt', 'fcv'],
    'rule->@name': ['wesdvgv', 'wefvsdv', 'reg', 'fbcdf'],
    'risk_level': ['3','4','2','1'],
    'risk_details': ['{}', '{}', '{}', '{}']}
        df = pd.DataFrame(data)
        self.ui = Impl_RiskWindow_from_Labeller(df, 1)

    def test_horizontalLayout(self):
        """Test the horizontal layouts in the window."""
        self.assertIsInstance(self.ui.hlayout, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout2, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout3, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout4, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout5, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout6, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout7, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout8, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout9, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout10, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout11, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout12, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout13, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout14, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout15, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout16, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout17, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout18, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout19, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout20, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout21, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout22, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout23, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout24, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout25, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout26, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout27, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout32, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout28, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout29, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout30, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout31, QtWidgets.QHBoxLayout)
        self.assertIsInstance(self.ui.hlayout33, QtWidgets.QHBoxLayout)
        
   
    def test_verticalLayout(self):
        """Test the vertical layouts in the window."""
        self.assertIsInstance(self.ui.vlayout, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout2, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout3, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout4, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout5, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout7, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout8, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout9, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout10, QtWidgets.QVBoxLayout)
        self.assertIsInstance(self.ui.vlayout11, QtWidgets.QVBoxLayout)
       
    def test_currentScoreGroup(self):
        """Test the newly added components of the 'Current Score' group box."""
        self.assertIsInstance(self.ui.btn_CancelClose,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_CancelClose.text(), "Cancel/Close")
        self.assertIsInstance(self.ui.btn_Help,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Help.text(), "Help")

    def test_groupBox4(self):
        """Test the newly added components of the new group box."""
        self.assertIsInstance(self.ui.btn_SaveScore,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_SaveScore.text(), "Save Score")
        self.assertIsInstance(self.ui.btn_SaveResults,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_SaveResults.text(), "Save Results")

    def test_groupBox3(self):
        """Test the newly added components of the new group box."""
        self.assertIsInstance(self.ui.btn_Page_1, QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_1.text(), "")
        self.assertIsInstance(self.ui.btn_Page_2, QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_2.text(), "")
        self.assertIsInstance(self.ui.tbl_CurrentExample,QtWidgets.QTableWidget)
        self.assertIsInstance(self.ui.btn_Page_3,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_3.text(), "")
        self.assertIsInstance(self.ui.btn_Page_4,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_4.text(), "")
        self.assertIsInstance(self.ui.btn_Page_5,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_5.text(), "")
        self.assertIsInstance(self.ui.btn_Page_6,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_6.text(), "")
        self.assertIsInstance(self.ui.btn_Page_7,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_7.text(), "")
        self.assertIsInstance(self.ui.btn_Page_8,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_8.text(), "")
        self.assertIsInstance(self.ui.btn_Page_9,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_9.text(), "")
        self.assertIsInstance(self.ui.btn_Page_10,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_10.text(), "")
        self.assertIsInstance(self.ui.btn_Page_11,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_11.text(), "")
        self.assertIsInstance(self.ui.btn_Page_12,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_12.text(), "")
        self.assertIsInstance(self.ui.btn_Page_13,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_13.text(), "")
        self.assertIsInstance(self.ui.btn_Page_14,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_14.text(), "")
        self.assertIsInstance(self.ui.btn_Page_15,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_15.text(), "")
        self.assertIsInstance(self.ui.btn_Page_16,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_16.text(), "")
        self.assertIsInstance(self.ui.btn_Page_17,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_17.text(), "")
        self.assertIsInstance(self.ui.btn_Page_18,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_18.text(), "")
        self.assertIsInstance(self.ui.btn_Page_19,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_19.text(), "")
        self.assertIsInstance(self.ui.btn_Page_20,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_20.text(), "")
        self.assertIsInstance(self.ui.btn_Page_21,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_21.text(), "")
        self.assertIsInstance(self.ui.btn_Page_22,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_22.text(), "")
        self.assertIsInstance(self.ui.btn_Page_23,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_23.text(), "")
        self.assertIsInstance(self.ui.btn_Page_24,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_24.text(), "")
        self.assertIsInstance(self.ui.btn_Page_25,QtWidgets.QPushButton)
        self.assertEqual(self.ui.btn_Page_25.text(), "")



    
    def test_HelpFeature(self):
        """Test the help feature in the window."""
        self.assertIsInstance(self.ui.btn_Help, QtWidgets.QPushButton)
        QTest.mouseClick(self.ui.btn_Help, Qt.LeftButton)
        

if __name__ == "__main__":
    unittest.main()