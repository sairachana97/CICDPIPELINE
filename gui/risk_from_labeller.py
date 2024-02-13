import os
from risk_predictions import Impl_RiskPredictionsWindow
from risk_model import Impl_RiskModelWindow
from help import Impl_HelpWindow
import numpy as np
from PyQt5 import QtCore, QtWidgets
from risk_from_labeller_ui import Ui_RiskWindow_from_Labeller
from risk_info import Impl_RiskInfoWindow
from vinci_utils import CWSS_DATA
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QWidget
import pandas as pd
import json
from dataset_column import DatasetColumn
import math
from PyQt5.QtCore import pyqtSignal

class Impl_RiskWindow_from_Labeller(Ui_RiskWindow_from_Labeller, QtWidgets.QMainWindow):
    """Creates risk assessment window"""

    total_risk_list = []
    def __init__(self, datasetDF, currentIdx, path):
        """Initializes risk window object"""
        super(Ui_RiskWindow_from_Labeller, self).__init__()
        self.setupUi(self)
        self.op_str = ""
        self.datasetDF = datasetDF
        self.currentSample = self.datasetDF.iloc[[currentIdx]]
        self.currentIdx = currentIdx
        self.path = path

        self.customInit()
        self.customEvents()

        for i in range(len(self.currentSample.columns.tolist())):
            if "path" in self.currentSample.columns.tolist()[i].lower():
                self.cBox_FindingFilepath.setCurrentIndex(i)
                break

    risk_list_signal = QtCore.pyqtSignal(list)

    def customInit(self):
        """Custom init method"""
        self.clearAll()
        self.fillCurrentSampleData()
        self.fillCWSSData()
        self.calculateRisk()

        self.cBox_GL_File.addItems(
            ["Disabled"] + self.currentSample.columns.tolist()
        )
        self.cBox_GL_Folder.addItems(
            ["Disabled"] + self.currentSample.columns.tolist()
        )
        self.cBox_GL_Values.addItems(self.currentSample.columns.tolist())

        self.cBox_FindingFilepath.addItems(self.currentSample.columns.tolist())

        self.gl_Values = []

        self.lbls_Page = [
            self.lbl_Page_1, self.lbl_Page_2, self.lbl_Page_3, self.lbl_Page_4, self.lbl_Page_5,
            self.lbl_Page_6, self.lbl_Page_7, self.lbl_Page_8, self.lbl_Page_9, self.lbl_Page_10,
            self.lbl_Page_11, self.lbl_Page_12, self.lbl_Page_13, self.lbl_Page_14, self.lbl_Page_15,
            self.lbl_Page_16, self.lbl_Page_17, self.lbl_Page_18, self.lbl_Page_19, self.lbl_Page_20,
            self.lbl_Page_21, self.lbl_Page_22, self.lbl_Page_23, self.lbl_Page_24, self.lbl_Page_25,
        ]
        self.btns_Page = [
            self.btn_Page_1, self.btn_Page_2, self.btn_Page_3, self.btn_Page_4, self.btn_Page_5,
            self.btn_Page_6, self.btn_Page_7, self.btn_Page_8, self.btn_Page_9, self.btn_Page_10,
            self.btn_Page_11, self.btn_Page_12, self.btn_Page_13, self.btn_Page_14, self.btn_Page_15,
            self.btn_Page_16, self.btn_Page_17, self.btn_Page_18, self.btn_Page_19, self.btn_Page_20,
            self.btn_Page_21, self.btn_Page_22, self.btn_Page_23, self.btn_Page_24, self.btn_Page_25,
        ]

        self.n_samples_labeling = self.datasetDF.shape[0]
        self.lbl_MaxNumSamples.setText("/{}".format(self.n_samples_labeling))
        self.sBox_CurrentSample.setMaximum(self.n_samples_labeling)
        self.sBox_CurrentSample.setMinimum(1)
        self.sBox_CurrentSample.setValue(self.currentIdx)
        self.sBox_CurrentSample.setEnabled(True)

        self.btn_FileTooltip.setToolTip("Select a filepath-like feature.\nFor example:\n- filepath\n- file\n- path\n\nAll samples on the same file \nwill be labeled the same.")
        self.btn_FolderTooltip.setToolTip("Select a folderpath-like feature.\nCould be the same as file.\nFor example:\n- filepath\n- file\n- path\n\nAll samples on the same folder \nwill be labeled the same.")
        self.btn_ValuesTooltip.setToolTip("Select some additional features.\nAll samples with the same values for these\nfeatures will be labeled the same.")
        self.btn_FindingFilepathTooltip.setToolTip("Select the column that specifies the path.\nFor example:\n- filepath\n- file\n- path")

        self.numPages = int(self.n_samples_labeling/25)+1
        self.lbl_PageMaxNumber.setText("/{}".format(self.numPages))
        self.sBox_Page.setMaximum(self.numPages)
        self.sBox_Page.setMinimum(1)
        self.sBox_Page.setValue(1)
        self.sBox_Page.setEnabled(True)
        self.updatePageSamples()
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.btn_SaveResults.setEnabled(False)
        self.btn_SaveSchema.setEnabled(False)
        self.btn_Model.setEnabled(False)
        self.btn_Predict.setEnabled(False)

    def customEvents(self):
        """Custom events method; here you connect functions with the UI."""
        self.home_button.triggered.connect(self.home_button_clicked)
        self.go_back_button.triggered.connect(self.go_back_button_clicked)

        self.cBox_BF_AL.currentTextChanged.connect(
            self.cBox_BF_AL_currentTextChanged
        )
        self.cBox_BF_AP.currentTextChanged.connect(
            self.cBox_BF_AP_currentTextChanged
        )
        self.cBox_BF_FC.currentTextChanged.connect(
            self.cBox_BF_FC_currentTextChanged
        )
        self.cBox_BF_IC.currentTextChanged.connect(
            self.cBox_BF_IC_currentTextChanged
        )
        self.cBox_BF_TI.currentTextChanged.connect(
            self.cBox_BF_TI_currentTextChanged
        )

        self.cBox_AS_AS.currentTextChanged.connect(
            self.cBox_AS_AS_currentTextChanged
        )
        self.cBox_AS_AV.currentTextChanged.connect(
            self.cBox_AS_AV_currentTextChanged
        )
        self.cBox_AS_IN.currentTextChanged.connect(
            self.cBox_AS_IN_currentTextChanged
        )
        self.cBox_AS_RL.currentTextChanged.connect(
            self.cBox_AS_RL_currentTextChanged
        )
        self.cBox_AS_RP.currentTextChanged.connect(
            self.cBox_AS_RP_currentTextChanged
        )
        self.cBox_AS_SC.currentTextChanged.connect(
            self.cBox_AS_SC_currentTextChanged
        )

        self.cBox_E_BI.currentTextChanged.connect(
            self.cBox_E_BI_currentTextChanged
        )
        self.cBox_E_DI.currentTextChanged.connect(
            self.cBox_E_DI_currentTextChanged
        )
        self.cBox_E_EC.currentTextChanged.connect(
            self.cBox_E_EC_currentTextChanged
        )
        self.cBox_E_EX.currentTextChanged.connect(
            self.cBox_E_EX_currentTextChanged
        )
        self.cBox_E_P.currentTextChanged.connect(
            self.cBox_E_P_currentTextChanged
        )

        self.cBox_GL_File.currentTextChanged.connect(
            self.cBox_GL_File_currentTextChanged
        )
        self.cBox_GL_Folder.currentTextChanged.connect(
            self.cBox_GL_Folder_currentTextChanged
        )
        self.cBox_FindingFilepath.currentTextChanged.connect(
            self.cBox_FindingFilepath_currentTextChanged
        )

        self.sBox_CurrentSample.valueChanged.connect(self.sBox_CurrentSample_valueChanged)
        self.sBox_Page.valueChanged.connect(self.sBox_Page_valueChanged)

        self.btn_GL_Add.clicked.connect(self.btn_GL_Add_clicked)
        self.btn_GL_Remove.clicked.connect(self.btn_GL_Remove_clicked)
        self.btn_CancelClose.clicked.connect(self.btn_CancelClose_clicked)
        self.btn_SaveScore.clicked.connect(self.btn_SaveScore_clicked)
        self.btn_SaveSchema.clicked.connect(self.btn_SaveSchema_clicked)
        #self.btn_LearnMore.clicked.connect(self.btn_LearnMore_clicked)
        self.btn_Help.clicked.connect(self.btn_Help_clicked)
        self.btn_SaveResults.clicked.connect(self.btn_SaveResults_clicked)
        self.btn_PrevLabeling.clicked.connect(self.btn_PrevLabeling_clicked)
        self.btn_NextLabeling.clicked.connect(self.btn_NextLabeling_clicked)
        self.btn_Model.clicked.connect(self.btn_Model_clicked)
        self.btn_Predict.clicked.connect(self.btn_Predict_clicked)

        for b in self.btns_Page:
            b.clicked.connect(self.btn_Page_clicked)

    def cBox_GL_File_currentTextChanged(self):
        filepathCol = self.cBox_GL_File.currentText()
        if filepathCol.lower() not in ["", "disabled"]:
            self.txtB_GL_Filepath.setText(str(self.currentSample[filepathCol].values[0]))
        else:
            self.txtB_GL_Filepath.setText("")
        
    def cBox_GL_Folder_currentTextChanged(self):
        folderpathCol = self.cBox_GL_Folder.currentText()
        if folderpathCol.lower() not in ["", "disabled"]:
            self.txtB_GL_Folderpath.setText(os.path.dirname(str(self.currentSample[folderpathCol].values[0])))
        else:
            self.txtB_GL_Folderpath.setText("")

    def cBox_FindingFilepath_currentTextChanged(self):
        filepathCol = self.cBox_FindingFilepath.currentText()
        if filepathCol.lower() not in ["", "disabled"]:
            self.txtB_FindingFilepath.setText(str(self.currentSample[filepathCol].values[0]))
        else:
            self.txtB_FindingFilepath.setText("")

    def btn_Page_clicked(self):
        btn = self.sender()
        btn_name = btn.objectName()
        btn_idx = int(btn_name.split("_")[-1])
        curr_sample_idx = (self.sBox_Page.value() - 1) * 25 + btn_idx
        self.sBox_CurrentSample.setValue(curr_sample_idx)

    def sBox_Page_valueChanged(self):
        self.updatePageSamples()

    def updatePageSamples(self):
        if self.sBox_Page.value() == self.numPages:
            for i in range(25 - self.n_samples_labeling % 25):
                self.btns_Page[-i-1].setText("")
                self.btns_Page[-i-1].setEnabled(False)
                self.btns_Page[-i-1].setStyleSheet("background-color: gray")
            for i in range(self.n_samples_labeling % 25):
                self.btns_Page[i].setEnabled(True)
        else:
            for i in range(25):
                self.btns_Page[i].setEnabled(True)

        currPage = self.sBox_Page.value()

        for i in range(25):
            self.lbls_Page[i].setText("{}".format((currPage-1)*25+i+1))

        for i in range(25):
            if (currPage-1)*25 + i >= self.n_samples_labeling:
                break
            if self.datasetDF.iloc[(currPage-1)*25+i]["risk_level"].lower() == "none":
                self.btns_Page[i].setText("R")
                self.btns_Page[i].setStyleSheet("background-color: palegreen")
            elif self.datasetDF.iloc[(currPage-1)*25+i]["risk_level"].lower() == "low":
                self.btns_Page[i].setText("R")
                self.btns_Page[i].setStyleSheet("background-color: khaki")
            elif self.datasetDF.iloc[(currPage-1)*25+i]["risk_level"].lower() == "medium":
                self.btns_Page[i].setText("R")
                self.btns_Page[i].setStyleSheet("background-color: orange")
            elif self.datasetDF.iloc[(currPage-1)*25+i]["risk_level"].lower() == "high":
                self.btns_Page[i].setText("R")
                self.btns_Page[i].setStyleSheet("background-color: orangered")
            elif self.datasetDF.iloc[(currPage-1)*25+i]["risk_level"].lower() == "critical":
                self.btns_Page[i].setText("R")
                self.btns_Page[i].setStyleSheet("background-color: red")
            else:
                self.btns_Page[i].setText("")
                self.btns_Page[i].setStyleSheet("background-color: white")

    def sBox_CurrentSample_valueChanged(self):
        self.currentIdx = int(self.sBox_CurrentSample.value()) - 1
        self.currentSample = self.datasetDF.iloc[[self.currentIdx]]
        self.displayProgress()
        self.fillCurrentSampleData()
        self.updatePageSamples()

    def count_Disabled_Button_Page(self):
        self.count = 0
        for i in range(25):
            if len( self.btns_Page[i].text()) > 0:
                self.count += 1 
    
    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
        Loads and show Help Window.
        """
        self.hs_ui = Impl_HelpWindow("Risk")
        self.hs_ui.show()
        
    def btn_GL_Add_clicked(self):
        curVal = self.cBox_GL_Values.currentText()
        if curVal not in self.gl_Values:
            self.gl_Values.append(curVal)
        self.txtB_GL_Values.setText("\n".join(self.gl_Values))

    def btn_GL_Remove_clicked(self):
        curVal = self.cBox_GL_Values.currentText()
        if curVal in self.gl_Values:
            self.gl_Values.remove(curVal)
        self.txtB_GL_Values.setText("\n".join(self.gl_Values))

    def btn_LearnMore_clicked(self):
        """Clicked event on btn_LearnMore component.
        Loads and shows Risk Info Window.
        """
        self.ri_ui = Impl_RiskInfoWindow()
        self.ri_ui.show()

    def fillCurrentSampleData(self):
        self.tbl_CurrentExample.clearContents()
        self.tbl_CurrentExample.setRowCount(0)
        cols = self.currentSample.columns.tolist()
        for col in cols:
            new_row_idx = self.tbl_CurrentExample.rowCount()
            self.tbl_CurrentExample.insertRow(new_row_idx)

            self.tbl_CurrentExample.setItem(
                new_row_idx, 0, QtWidgets.QTableWidgetItem(col)
            )
            self.tbl_CurrentExample.setItem(
                new_row_idx,
                1,
                QtWidgets.QTableWidgetItem(
                    str(self.currentSample[col].values[0])
                ),
            )

    def btn_SaveScore_clicked(self):
        idxs = self.findSamplesGroup()
        risk_list = self.createRiskList(idxs)
        if len(idxs) > 1:
            response = QMessageBox.question(
                self,
                "Save Risk Labels",
                "You are going to label {} samples simultaneously.\nContinue?".format(
                    len(idxs)
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if response == QMessageBox.Yes:
                self.risk_list_signal.emit(risk_list)
        else:
            self.risk_list_signal.emit(risk_list)
        self.currentSample = self.datasetDF.iloc[[self.currentIdx]]
        self.fillCurrentSampleData()
        self.updatePageSamples()
        self.btn_SaveResults.setEnabled(True)

    def btn_SaveResults_clicked(self):
        """Saves previously produced inference results to a CSV file."""
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            widget,
            "Save Risk Results File",
            "",
            "CSV Files (*.csv)",
            options=options,
        )
        if fileName:
            fileName = (
                fileName + ".csv" if not fileName.endswith(".csv") else fileName
            )
            idxs = self.findSamplesGroup()
            risk_list = self.createRiskList(idxs)

            self.results_df = self.datasetDF
            self.results_df.to_csv(fileName)
            self.btn_SaveScore.setEnabled(False)
            self.btn_SaveSchema.setEnabled(True)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Results saved successfully at {}".format(fileName))
            msg.setWindowTitle("Results saved!")
            msg.exec_()
            self.btn_Model.setEnabled(True)
            self.btn_Predict.setEnabled(True)

    def btn_SaveSchema_clicked(self):
        """clicked event on btn_Schema
        Saves current schema to a json file at specified location.
        """
        self.trainPercentage = 10
        self.testPercentage = 90
        self.datasetColumns = []
        for c in self.datasetDF.columns:
            dsCol = DatasetColumn.fromdict1(c)
            self.datasetColumns.append(dsCol)
        self.dataset_type = "csv"
        numColumns = len(self.datasetColumns)
        if numColumns == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Not enough columns!")
            msg.setText(
                "Please, make sure that you have at least one input and one output columns."
            )
            msg.exec_()
            return
        numOutputColumns = len(
            [c for c in self.datasetColumns if c.Type == "Output"]
        )
        if numOutputColumns != 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Wrong output column!")
            msg.setText(
                "Please, make sure that you have a single output column."
            )
            msg.exec_()
            return
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            widget,
            "Save Schema File",
            "",
            "JSON Files (*.json)",
            options=options,
        )
        if fileName:
            fileName = (
                fileName + ".json"
                if not fileName.endswith(".json")
                else fileName
            )
            if self.dataset_type == "csv":
                jsonDict = DatasetColumn.CreateRiskJson(
                    self.datasetColumns,
                    self.trainPercentage,
                    self.datasetDF,
                )
            with open(fileName, "w", encoding="utf-8") as fp:
                json.dump(jsonDict, fp)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File saved successfully!")
            msg.setWindowTitle("File saved")
            msg.exec_()

    def btn_CancelClose_clicked(self):
        self.close()

    def findSamplesGroup(self):
        singleLabel = True
        sameFile = self.cBox_GL_File.currentText()
        sameFolder = self.cBox_GL_Folder.currentText()
        sameValues = self.gl_Values

        if sameFile.lower() == "disabled":
            sameFileMask = np.full(self.datasetDF.shape[0], True)
        else:
            singleLabel = False
            sameFileMask = (
                self.datasetDF[sameFile]
                == self.currentSample[sameFile].values[0]
            )

        if sameFolder.lower() == "disabled":
            sameFolderMask = np.full(self.datasetDF.shape[0], True)
        else:
            singleLabel = False
            sameFolderMask = (
                self.datasetDF[sameFolder].apply(
                    lambda path: os.path.dirname(path)
                )
                == self.currentSample[sameFolder]
                .apply(lambda path: os.path.dirname(path))
                .values[0]
            )

        sameValuesMask = np.full(self.datasetDF.shape[0], True)
        for val in sameValues:
            singleLabel = False
            sameValuesMask = sameValuesMask & (
                self.datasetDF[val] == self.currentSample[val].values[0]
            )

        if singleLabel:
            index_list = [self.currentIdx]
        else:
            groupMask = sameFileMask & sameFolderMask & sameValuesMask
            index_list = self.datasetDF.index[groupMask].tolist()

        return index_list

    def createRiskList(self, idxs):
        (
            bf_score,
            as_score,
            e_score,
            final_score,
            risk_level,
        ) = self._calculateRisk()
        risk_list = []
        for idx in idxs:
            risk_list.append(
                {
                    "idx": idx,
                    "scores": {
                        "final": "{:.2f}".format(final_score),
                        "base_finding": "{:.2f}".format(bf_score),
                        "attack_surface": "{:.2f}".format(as_score),
                        "environmental": "{:.2f}".format(e_score),
                    },
                    "risk_level": risk_level,
                }
            )
        self.total_risk_list.append(risk_list)
        return self.total_risk_list

    def cBox_BF_AL_currentTextChanged(self):
        self.updateInfo(
            self.txtB_BF_AL_Letter,
            self.txtB_BF_AL_Value,
            "base_finding",
            "al",
            self.cBox_BF_AL.currentIndex(),
        )
        self.calculateRisk()

    def cBox_BF_AP_currentTextChanged(self):
        self.updateInfo(
            self.txtB_BF_AP_Letter,
            self.txtB_BF_AP_Value,
            "base_finding",
            "ap",
            self.cBox_BF_AP.currentIndex(),
        )
        self.calculateRisk()

    def cBox_BF_FC_currentTextChanged(self):
        self.updateInfo(
            self.txtB_BF_FC_Letter,
            self.txtB_BF_FC_Value,
            "base_finding",
            "fc",
            self.cBox_BF_FC.currentIndex(),
        )
        self.calculateRisk()

    def cBox_BF_IC_currentTextChanged(self):
        self.updateInfo(
            self.txtB_BF_IC_Letter,
            self.txtB_BF_IC_Value,
            "base_finding",
            "ic",
            self.cBox_BF_IC.currentIndex(),
        )
        self.calculateRisk()

    def cBox_BF_TI_currentTextChanged(self):
        self.updateInfo(
            self.txtB_BF_TI_Letter,
            self.txtB_BF_TI_Value,
            "base_finding",
            "ti",
            self.cBox_BF_TI.currentIndex(),
        )
        self.calculateRisk()

    def cBox_AS_AS_currentTextChanged(self):
        self.updateInfo(
            self.txtB_AS_AS_Letter,
            self.txtB_AS_AS_Value,
            "attack_surface",
            "as",
            self.cBox_AS_AS.currentIndex(),
        )
        self.calculateRisk()

    def cBox_AS_AV_currentTextChanged(self):
        self.updateInfo(
            self.txtB_AS_AV_Letter,
            self.txtB_AS_AV_Value,
            "attack_surface",
            "av",
            self.cBox_AS_AV.currentIndex(),
        )
        self.calculateRisk()

    def cBox_AS_IN_currentTextChanged(self):
        self.updateInfo(
            self.txtB_AS_IN_Letter,
            self.txtB_AS_IN_Value,
            "attack_surface",
            "in",
            self.cBox_AS_IN.currentIndex(),
        )
        self.calculateRisk()

    def cBox_AS_RL_currentTextChanged(self):
        self.updateInfo(
            self.txtB_AS_RL_Letter,
            self.txtB_AS_RL_Value,
            "attack_surface",
            "rl",
            self.cBox_AS_RL.currentIndex(),
        )
        self.calculateRisk()

    def cBox_AS_RP_currentTextChanged(self):
        self.updateInfo(
            self.txtB_AS_RP_Letter,
            self.txtB_AS_RP_Value,
            "attack_surface",
            "rp",
            self.cBox_AS_RP.currentIndex(),
        )
        self.calculateRisk()

    def cBox_AS_SC_currentTextChanged(self):
        self.updateInfo(
            self.txtB_AS_SC_Letter,
            self.txtB_AS_SC_Value,
            "attack_surface",
            "sc",
            self.cBox_AS_SC.currentIndex(),
        )
        self.calculateRisk()

    def cBox_E_BI_currentTextChanged(self):
        self.updateInfo(
            self.txtB_E_BI_Letter,
            self.txtB_E_BI_Value,
            "environmental",
            "bi",
            self.cBox_E_BI.currentIndex(),
        )
        self.calculateRisk()

    def cBox_E_DI_currentTextChanged(self):
        self.updateInfo(
            self.txtB_E_DI_Letter,
            self.txtB_E_DI_Value,
            "environmental",
            "di",
            self.cBox_E_DI.currentIndex(),
        )
        self.calculateRisk()

    def cBox_E_EC_currentTextChanged(self):
        self.updateInfo(
            self.txtB_E_EC_Letter,
            self.txtB_E_EC_Value,
            "environmental",
            "ec",
            self.cBox_E_EC.currentIndex(),
        )
        self.calculateRisk()

    def cBox_E_EX_currentTextChanged(self):
        self.updateInfo(
            self.txtB_E_EX_Letter,
            self.txtB_E_EX_Value,
            "environmental",
            "ex",
            self.cBox_E_EX.currentIndex(),
        )
        self.calculateRisk()

    def cBox_E_P_currentTextChanged(self):
        self.updateInfo(
            self.txtB_E_P_Letter,
            self.txtB_E_P_Value,
            "environmental",
            "p",
            self.cBox_E_P.currentIndex(),
        )
        self.calculateRisk()

    def btn_PrevLabeling_clicked(self):
        """clicked event on btn_PrevLabeling
        Sets previous data sample as current if valid.
        """
        curr = int(self.sBox_CurrentSample.value())
        currPage = int(self.sBox_Page.value())
        if curr - 1 > 0:
            self.sBox_CurrentSample.setValue(curr - 1)
            newPage = int(math.ceil((curr - 1)/25))
            if newPage != currPage:
                self.sBox_Page.setValue(newPage)

        idxs = self.findSamplesGroup()
        risk_list = self.createRiskList(idxs)
        if len(idxs) > 1:
            response = QMessageBox.question(
                self,
                "Save Risk Labels",
                "You are going to label {} samples simultaneously.\nContinue?".format(
                    len(idxs)
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if response == QMessageBox.Yes:
                self.risk_list_signal.emit(risk_list)
        else:
            self.risk_list_signal.emit(risk_list)
        self.currentSample = self.datasetDF.iloc[[self.currentIdx]]
        self.fillCurrentSampleData()
        self.updatePageSamples()
        self.btn_SaveResults.setEnabled(True)

    def btn_NextLabeling_clicked(self):
        """clicked event on btn_NextLabeling
        Sets next data sample as current if valid.
        """

        curr = int(self.sBox_CurrentSample.value())
        currPage = int(self.sBox_Page.value())
        if curr + 1 <= self.n_samples_labeling:
            self.sBox_CurrentSample.setValue(curr + 1)
            newPage = int(math.ceil((curr + 1)/25))
            if newPage != currPage:
                self.sBox_Page.setValue(newPage)
        
        idxs = self.findSamplesGroup()
        risk_list = self.createRiskList(idxs)
        if len(idxs) > 1:
            response = QMessageBox.question(
                self,
                "Save Risk Labels",
                "You are going to label {} samples simultaneously.\nContinue?".format(
                    len(idxs)
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if response == QMessageBox.Yes:
                self.risk_list_signal.emit(risk_list)
        else:
            self.risk_list_signal.emit(risk_list)
        self.currentSample = self.datasetDF.iloc[[self.currentIdx]]
        self.fillCurrentSampleData()
        self.updatePageSamples()
        self.btn_SaveResults.setEnabled(True)

    def displayProgress(self):
        """Displays labeling progress."""
        self.labels = [-1 for _ in range(self.n_samples_labeling)]
        self.count_Disabled_Button_Page()
        n_labeled = self.n_samples_labeling - self.labels.count(-1)
        self.lbl_Progress.setText(
            "Progress: {}/{}".format(self.count + 1, self.n_samples_labeling)
        )
        self.lbl_ProgressPerc.setText(
            "({:.2f} %)".format(100.0 * (self.count + 1) / self.n_samples_labeling)
        )
    
    def btn_Model_clicked(self):
        """Clicked event on btn_Model component.
        Loads and shows Risk Model Window.
        """
        self.rm_ui = Impl_RiskModelWindow(self.results_df)
        self.rm_ui.show()

    def btn_Predict_clicked(self):
        """Clicked event on btn_Predict component.
        Loads and shows Risk Prediction Window.
        """
        self.rm_ui = Impl_RiskPredictionsWindow()
        self.rm_ui.show()

    def clearAll(self):
        """Clears all elements from combo boxes and clears strings from text boxes."""
        self.cBox_GL_File.clear()
        self.cBox_GL_Folder.clear()
        self.cBox_GL_Values.clear()
        # Base Finding
        self.cBox_BF_AL.clear()
        self.txtB_BF_AL_Letter.setText("")
        self.txtB_BF_AL_Value.setText("")
        self.cBox_BF_AP.clear()
        self.txtB_BF_AP_Letter.setText("")
        self.txtB_BF_AP_Value.setText("")
        self.cBox_BF_FC.clear()
        self.txtB_BF_FC_Letter.setText("")
        self.txtB_BF_FC_Value.setText("")
        self.cBox_BF_IC.clear()
        self.txtB_BF_IC_Letter.setText("")
        self.txtB_BF_IC_Value.setText("")
        self.cBox_BF_TI.clear()
        self.txtB_BF_TI_Letter.setText("")
        self.txtB_BF_TI_Value.setText("")
        # Attack Surface
        self.cBox_AS_AS.clear()
        self.txtB_AS_AS_Letter.setText("")
        self.txtB_AS_AS_Value.setText("")
        self.cBox_AS_AV.clear()
        self.txtB_AS_AV_Letter.setText("")
        self.txtB_AS_AV_Value.setText("")
        self.cBox_AS_IN.clear()
        self.txtB_AS_IN_Letter.setText("")
        self.txtB_AS_IN_Value.setText("")
        self.cBox_AS_RL.clear()
        self.txtB_AS_RL_Letter.setText("")
        self.txtB_AS_RL_Value.setText("")
        self.cBox_AS_RP.clear()
        self.txtB_AS_RP_Letter.setText("")
        self.txtB_AS_RP_Value.setText("")
        self.cBox_AS_SC.clear()
        self.txtB_AS_SC_Letter.setText("")
        self.txtB_AS_SC_Value.setText("")
        # Environmental
        self.cBox_E_BI.clear()
        self.txtB_E_BI_Letter.setText("")
        self.txtB_E_BI_Value.setText("")
        self.cBox_E_DI.clear()
        self.txtB_E_DI_Letter.setText("")
        self.txtB_E_DI_Value.setText("")
        self.cBox_E_EC.clear()
        self.txtB_E_EC_Letter.setText("")
        self.txtB_E_EC_Value.setText("")
        self.cBox_E_EX.clear()
        self.txtB_E_EX_Letter.setText("")
        self.txtB_E_EX_Value.setText("")
        self.cBox_E_P.clear()
        self.txtB_E_P_Letter.setText("")
        self.txtB_E_P_Value.setText("")

    def btn_Model_clicked(self):
        self.hs_ui = Impl_RiskModelWindow(self.datasetDF)
        self.hs_ui.show()

    def fillCWSSData(self):
        """Fills all combo boxes with its possible items.
        After that, selects "Default" on every option and sets its letter and value.
        """
        # Base Finding
        self.cBox_BF_AL.addItems(CWSS_DATA["base_finding"]["al"]["selections"])
        self.cBox_BF_AP.addItems(CWSS_DATA["base_finding"]["ap"]["selections"])
        self.cBox_BF_FC.addItems(CWSS_DATA["base_finding"]["fc"]["selections"])
        self.cBox_BF_IC.addItems(CWSS_DATA["base_finding"]["ic"]["selections"])
        self.cBox_BF_TI.addItems(CWSS_DATA["base_finding"]["ti"]["selections"])
        # Attack Surface
        self.cBox_AS_AS.addItems(
            CWSS_DATA["attack_surface"]["as"]["selections"]
        )
        self.cBox_AS_AV.addItems(
            CWSS_DATA["attack_surface"]["av"]["selections"]
        )
        self.cBox_AS_IN.addItems(
            CWSS_DATA["attack_surface"]["in"]["selections"]
        )
        self.cBox_AS_RL.addItems(
            CWSS_DATA["attack_surface"]["rl"]["selections"]
        )
        self.cBox_AS_RP.addItems(
            CWSS_DATA["attack_surface"]["rp"]["selections"]
        )
        self.cBox_AS_SC.addItems(
            CWSS_DATA["attack_surface"]["sc"]["selections"]
        )
        # Environmental
        self.cBox_E_BI.addItems(CWSS_DATA["environmental"]["bi"]["selections"])
        self.cBox_E_DI.addItems(CWSS_DATA["environmental"]["di"]["selections"])
        self.cBox_E_EC.addItems(CWSS_DATA["environmental"]["ec"]["selections"])
        self.cBox_E_EX.addItems(CWSS_DATA["environmental"]["ex"]["selections"])
        self.cBox_E_P.addItems(CWSS_DATA["environmental"]["p"]["selections"])

        # Base Finding
        def_idx = CWSS_DATA["base_finding"]["al"]["selections"].index(
            "Default"
        )
        self.cBox_BF_AL.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_BF_AL_Letter,
            self.txtB_BF_AL_Value,
            "base_finding",
            "al",
            def_idx,
        )
        def_idx = CWSS_DATA["base_finding"]["ap"]["selections"].index(
            "Default"
        )
        self.cBox_BF_AP.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_BF_AP_Letter,
            self.txtB_BF_AP_Value,
            "base_finding",
            "ap",
            def_idx,
        )
        def_idx = CWSS_DATA["base_finding"]["fc"]["selections"].index(
            "Default"
        )
        self.cBox_BF_FC.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_BF_FC_Letter,
            self.txtB_BF_FC_Value,
            "base_finding",
            "fc",
            def_idx,
        )
        def_idx = CWSS_DATA["base_finding"]["ic"]["selections"].index(
            "Default"
        )
        self.cBox_BF_IC.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_BF_IC_Letter,
            self.txtB_BF_IC_Value,
            "base_finding",
            "ic",
            def_idx,
        )
        def_idx = CWSS_DATA["base_finding"]["ti"]["selections"].index(
            "Default"
        )
        self.cBox_BF_TI.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_BF_TI_Letter,
            self.txtB_BF_TI_Value,
            "base_finding",
            "ti",
            def_idx,
        )
        # Attack Surface
        def_idx = CWSS_DATA["attack_surface"]["as"]["selections"].index(
            "Default"
        )
        self.cBox_AS_AS.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_AS_AS_Letter,
            self.txtB_AS_AS_Value,
            "attack_surface",
            "as",
            def_idx,
        )
        def_idx = CWSS_DATA["attack_surface"]["av"]["selections"].index(
            "Default"
        )
        self.cBox_AS_AV.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_AS_AV_Letter,
            self.txtB_AS_AV_Value,
            "attack_surface",
            "av",
            def_idx,
        )
        def_idx = CWSS_DATA["attack_surface"]["in"]["selections"].index(
            "Default"
        )
        self.cBox_AS_IN.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_AS_IN_Letter,
            self.txtB_AS_IN_Value,
            "attack_surface",
            "in",
            def_idx,
        )
        def_idx = CWSS_DATA["attack_surface"]["rl"]["selections"].index(
            "Default"
        )
        self.cBox_AS_RL.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_AS_RL_Letter,
            self.txtB_AS_RL_Value,
            "attack_surface",
            "rl",
            def_idx,
        )
        def_idx = CWSS_DATA["attack_surface"]["rp"]["selections"].index(
            "Default"
        )
        self.cBox_AS_RP.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_AS_RP_Letter,
            self.txtB_AS_RP_Value,
            "attack_surface",
            "rp",
            def_idx,
        )
        def_idx = CWSS_DATA["attack_surface"]["sc"]["selections"].index(
            "Default"
        )
        self.cBox_AS_SC.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_AS_SC_Letter,
            self.txtB_AS_SC_Value,
            "attack_surface",
            "sc",
            def_idx,
        )
        # Environmental
        def_idx = CWSS_DATA["environmental"]["bi"]["selections"].index(
            "Default"
        )
        self.cBox_E_BI.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_E_BI_Letter,
            self.txtB_E_BI_Value,
            "environmental",
            "bi",
            def_idx,
        )
        def_idx = CWSS_DATA["environmental"]["di"]["selections"].index(
            "Default"
        )
        self.cBox_E_DI.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_E_DI_Letter,
            self.txtB_E_DI_Value,
            "environmental",
            "di",
            def_idx,
        )
        def_idx = CWSS_DATA["environmental"]["ec"]["selections"].index(
            "Default"
        )
        self.cBox_E_EC.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_E_EC_Letter,
            self.txtB_E_EC_Value,
            "environmental",
            "ec",
            def_idx,
        )
        def_idx = CWSS_DATA["environmental"]["ex"]["selections"].index(
            "Default"
        )
        self.cBox_E_EX.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_E_EX_Letter,
            self.txtB_E_EX_Value,
            "environmental",
            "ex",
            def_idx,
        )
        def_idx = CWSS_DATA["environmental"]["p"]["selections"].index(
            "Default"
        )
        self.cBox_E_P.setCurrentIndex(def_idx)
        self.updateInfo(
            self.txtB_E_P_Letter,
            self.txtB_E_P_Value,
            "environmental",
            "p",
            def_idx,
        )

    def updateInfo(self, txtB_letter, txtB_value, group, metric, cur_index):
        """Updates info of letter and value for the specified selection on group and metric.

        Args:
            txtB_letter (QLineEdit): Text box to set current selection letter value.
            txtB_value (QLineEdit): Text box to set current selection numerical value.
            group (str): Current metric group
            metric (str): Current metric
            cur_index (int): Selected index
        """
        txtB_letter.setText(CWSS_DATA[group][metric]["letters"][cur_index])
        txtB_value.setText(
            "{0:0.2f}".format(CWSS_DATA[group][metric]["values"][cur_index])
        )

    def _calculateRisk(self):
        """Calculates risk for base finding, attack surface and environmental metric groups.
        Then calculates final score and risk.
        """
        bf_ti = float(self.txtB_BF_TI_Value.text())
        bf_ap = float(self.txtB_BF_AP_Value.text())
        bf_al = float(self.txtB_BF_AL_Value.text())
        bf_ic = float(self.txtB_BF_IC_Value.text())
        bf_fc = float(self.txtB_BF_FC_Value.text())

        as_rp = float(self.txtB_AS_RP_Value.text())
        as_rl = float(self.txtB_AS_RL_Value.text())
        as_av = float(self.txtB_AS_AV_Value.text())
        as_as = float(self.txtB_AS_AS_Value.text())
        as_in = float(self.txtB_AS_IN_Value.text())
        as_sc = float(self.txtB_AS_SC_Value.text())

        e_bi = float(self.txtB_E_BI_Value.text())
        e_di = float(self.txtB_E_DI_Value.text())
        e_ex = float(self.txtB_E_EX_Value.text())
        e_ec = float(self.txtB_E_EC_Value.text())
        e_p = float(self.txtB_E_P_Value.text())

        if bf_ti == 0:
            bf_score = 0
        else:
            bf_score = (
                4 * bf_ic * (10 * bf_ti + 5 * (bf_ap + bf_al) + 5 * bf_fc)
            )

        as_score = (
            20 * (as_rp + as_rl + as_av) + 20 * as_sc + 15 * as_in + 5 * as_as
        ) / 100.0

        if e_bi == 0:
            e_score = 0
        else:
            e_score = e_ec / 20 * (10 * e_bi + 3 * e_di + 4 * e_ex + 3 * e_p)

        final_score = bf_score * as_score * e_score

        if final_score == 0:
            risk_level = "None"
        elif 0 < final_score < 55:
            risk_level = "Low"
        elif 55 <= final_score < 65:
            risk_level = "Medium"
        elif 65 <= final_score < 75:
            risk_level = "High"
        elif 75 < final_score <= 100:
            risk_level = "Critical"

        return bf_score, as_score, e_score, final_score, risk_level

    def calculateRisk(self):
        """Calculates risk for base finding, attack surface and environmental metric groups.
        Then calculates final score and risk and shows it on CWSS Score screen.
        """
        (
            bf_score,
            as_score,
            e_score,
            final_score,
            risk_level,
        ) = self._calculateRisk()

        self.txtB_CWSS_BF_info.setText("{0:0.2f}".format(bf_score))
        self.txtB_CWSS_AS_info.setText("{0:0.2f}".format(as_score))
        self.txtB_CWSS_E_info.setText("{0:0.2f}".format(e_score))
        self.txtB_CWSS_Score_info.setText("{0:0.2f}".format(final_score))
        self.txtB_CWSS_Threat_info.setText(risk_level)
    
    def home_button_clicked(self):
        from menu import Impl_MainWindow
        self.hm_ui = Impl_MainWindow()
        self.hm_ui.show()
        self.close()
        
    def go_back_button_clicked(self):
        from datasets_labeler import Impl_DatasetsLabelerWindow
        self.bw_ui = Impl_DatasetsLabelerWindow(self.path)
        self.bw_ui.show()
        self.close()
        