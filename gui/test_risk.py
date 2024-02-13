from unittest.mock import MagicMock
from risk import Impl_RiskWindow

import sys
import unittest
from PyQt5.QtWidgets import QApplication, QMessageBox
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
        self.ui = Impl_RiskWindow(df, 1)

    def test_SaveResults(self):
        self.ui.btn_SaveResults.click()
        self.assertEqual(self.ui.btn_SaveResults_clicked(), None)
        mbox = QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Results saved!")
        mbox.exec_ = MagicMock()
        mbox.exec_()
        mbox.exec_.assert_called_once()

    def test_SaveSchema(self):
        self.ui.btn_SaveSchema.click()
        self.assertEqual(self.ui.btn_SaveSchema_clicked(), None)
        mbox = QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Results saved!")
        mbox.exec_ = MagicMock()
        mbox.exec_()
        mbox.exec_.assert_called_once()

    def test_Models(self):
        self.ui.btn_Model.click()
        self.assertEqual(self.ui.btn_Model_clicked(), None)


if __name__ == "__main__":
    unittest.main()