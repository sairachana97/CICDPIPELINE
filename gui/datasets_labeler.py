import pandas as pd
import os
import json
import random
import math
from datasets_labeler_ui import Ui_DatasetsLabelerWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from risk_from_labeller import Impl_RiskWindow_from_Labeller
from groupLabelling import Impl_GroupLabelling_Window
from help import Impl_HelpWindow
from PyQt5.QtCore import pyqtSignal


class Impl_DatasetsLabelerWindow(
    Ui_DatasetsLabelerWindow, QtWidgets.QMainWindow
):
    """Creates datasets labeler window"""
    def __init__(self, datasetPath):
        """Initializes datasets window object"""
        super(Impl_DatasetsLabelerWindow, self).__init__()
        self.setupUi(self)
        self.path = datasetPath
        self.customInit()
        self.customEvents()

        self.loadDatasetFromCall(datasetPath)

    def customInit(self):
        """Custom init method"""
        self.sBox_SampleSize.setEnabled(False)
        self.dsBox_SamplePerc.setEnabled(False)
        self.sBox_CustomSeed.setEnabled(False)
        self.cBox_SampleType.clear()
        self.cBox_SampleType.addItems(["Random", "Ordered", "Stratified"])
        self.cBox_SampleType.setEnabled(False)
        self.btn_SaveSample.setEnabled(False)
        self.sBox_handle = "pct"
        self.df_dataset_sampling = None
        self.df_dataset_labeling = None
        self.currentLabel = self.rBtn_CurrentTrue.isChecked()
        self.numPages = 1
        self.seed = random.randint(0, 100000)
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

    def customEvents(self):
        """Custom events method; here you connect functions with the UI."""
        self.home_button.triggered.connect(self.home_button_clicked)
        self.go_back_button.triggered.connect(self.go_back_button_clicked)
        self.btn_LoadDatasetSampling.clicked.connect(
            self.btn_LoadDatasetSampling_clicked
        )
        self.btn_SaveSample.clicked.connect(self.btn_SaveSample_clicked)
        self.btn_LoadDatasetLabeling.clicked.connect(
            self.btn_LoadDatasetLabeling_clicked
        )
        self.btn_PrevLabeling.clicked.connect(self.btn_PrevLabeling_clicked)
        self.btn_NextLabeling.clicked.connect(self.btn_NextLabeling_clicked)
        self.btn_Help.clicked.connect(self.btn_Help_clicked)
        self.btn_SaveDatasetLabeling.clicked.connect(
            self.btn_SaveDatasetLabeling_clicked
        )
        self.btn_Risk.clicked.connect(self.btn_Risk_clicked)
        self.btn_GroupLabelling.clicked.connect(self.btn_GroupLabelling_clicked)

        self.txtB_ColumnLabel.textChanged.connect(
            self.txtB_ColumnLabel_textChanged
        )

        self.chkBox_CustomSeed.toggled.connect(self.chkBox_CustomSeed_toggled)

        self.cBox_SampleType.currentTextChanged.connect(
            self.cBox_SampleType_currentTextChanged
        )

        self.sBox_SampleSize.valueChanged.connect(
            self.sBox_SampleSize_valueChanged
        )
        self.dsBox_SamplePerc.valueChanged.connect(
            self.dsBox_SamplePerc_valueChanged
        )

        self.rBtn_Size.toggled.connect(self.rBtn_Size_toggled)
        self.rBtn_SizePerc.toggled.connect(self.rBtn_SizePerc_toggled)
        self.rBtn_CurrentTrue.toggled.connect(self.rBtn_CurrentTrue_toggled)
        self.rBtn_CurrentFalse.toggled.connect(self.rBtn_CurrentFalse_toggled)

        self.sBox_Sample.valueChanged.connect(self.sBox_Sample_valueChanged)
        self.sBox_Page.valueChanged.connect(self.sBox_Page_valueChanged)

        for b in self.btns_Page:
            b.clicked.connect(self.btn_Page_clicked)
    
    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
        Loads and show Help Window.
        """
        self.hs_ui = Impl_HelpWindow("Labeler")
        self.hs_ui.show()


    def pathReturn(self):
        return self.path

    def btn_Page_clicked(self):
        btn = self.sender()
        btn_name = btn.objectName()
        btn_idx = int(btn_name.split("_")[-1])
        curr_sample_idx = (self.sBox_Page.value() - 1) * 25 + btn_idx
        self.sBox_Sample.setValue(curr_sample_idx)

    def loadDatasetFromCall(self, datasetPath):
        if datasetPath != "":
            if datasetPath[-4:] == ".csv":
                self.loadDatasetSampling(datasetPath)
                self.loadDatasetLabeling(datasetPath)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Wrong dataset format")
                msg.setText(
                    "When labeling the selected dataset must be in .csv format.\nCurrent dataset will not be loaded."
                )
                msg.exec_()

    @QtCore.pyqtSlot(list)
    def saveRiskLabels(self, risk_list):
        for risk in risk_list:
            for entry in risk:
                idx = entry.pop("idx")
                risk_level = entry.pop("risk_level")
                self.df_dataset_labeling.at[idx, "risk_level"] = risk_level
        self.showExampleInTable(
            int(self.sBox_Sample.value()) - 1
        )  # As a way to refresh current saved risk level and details.
        self.updatePageSamples()

    @QtCore.pyqtSlot(list)
    def showSignal(self, risk_list):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Data sent from Risk Window")
        msg.setText(str(risk_list))
        msg.exec_()

    def btn_Risk_clicked(self):
        """Clicked event on btn_Risk component.
        Loads and shows Risk Window.
        """
        idx = int(self.sBox_Sample.value()) - 1
        self.rs_ui = Impl_RiskWindow_from_Labeller(self.df_dataset_labeling, idx, self.path)
        self.rs_ui.risk_list_signal.connect(self.saveRiskLabels)
        self.rs_ui.show()
        self.close()
            
    def receive_window_path(self, path):
        print("Received dataset path:", path)
        self.hide()
        try:
            # Assuming you want to open Impl_DatasetsLabelerWindow with the received path
            self.rs_ui = Impl_DatasetsLabelerWindow(self.path)
            self.rs_ui.show()
            if path == "home":
                print("clicked home button")
                self.home_button_clicked()
        except Exception as e:
            print(f"Error creating or showing Impl_DatasetsLabelerWindow: {e}")
        

    def btn_GroupLabelling_clicked(self):
        idx = int(self.sBox_Sample.value()) - 1
        datasetPath = self.path
        self.rs_ui = Impl_GroupLabelling_Window(datasetPath)
        self.rs_ui.show()
        self.close()

    def cBox_SampleType_currentTextChanged(self):
        """currentTextChanged event on cBox_SampleType
        Shows all columns available to become column reference for
        stratified sampling.
        """
        sample_type = self.cBox_SampleType.currentText()
        if (
            sample_type == "Stratified"
            and self.df_dataset_sampling is not None
        ):
            self.cBox_StratifiedReference.clear()
            self.cBox_StratifiedReference.addItems(
                self.df_dataset_sampling.columns.tolist()
            )
            self.cBox_StratifiedReference.setEnabled(True)
        else:
            self.cBox_StratifiedReference.clear()
            self.cBox_StratifiedReference.setEnabled(False)

    def rBtn_SizePerc_toggled(self):
        """toggled event on rBtn_SizePerc
        Enables sample size manipulation as percentage.
        """
        self.dsBox_SamplePerc.setEnabled(True)
        self.sBox_SampleSize.setEnabled(False)
        self.sBox_handle = "pct"

    def rBtn_Size_toggled(self):
        """toggled event on rBtn_Size
        Enables sample size manipulation as integers.
        """
        self.dsBox_SamplePerc.setEnabled(False)
        self.sBox_SampleSize.setEnabled(True)
        self.sBox_handle = "int"

    def dsBox_SamplePerc_valueChanged(self):
        """valueChanged event on dsBox_SamplePerc
        Displays new sample size when percentage changes.
        """
        if self.sBox_handle == "pct":
            new_int = int(
                round(
                    self.dsBox_SamplePerc.value()
                    * self.df_dataset_sampling.shape[0]
                    / 100.0,
                    0,
                )
            )
            self.sBox_SampleSize.setValue(new_int)

    def sBox_SampleSize_valueChanged(self):
        """valueChanged event on sBox_SampleSize
        Displays new sample size when number of samples changes.
        """
        if self.sBox_handle == "int":
            new_pct = round(
                100.0
                * float(self.sBox_SampleSize.value())
                / self.df_dataset_sampling.shape[0],
                2,
            )
            self.dsBox_SamplePerc.setValue(new_pct)

    def btn_SaveSample_clicked(self):
        """clicked event on btn_SaveSample
        Saves sample as csv to specified file location.
        """
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            widget,
            "Save Sampled CSV File",
            "",
            "CSV File (*.csv)",
            options=options,
        )
        if fileName:
            fileName = (
                fileName + ".csv"
                if not fileName.endswith(".csv")
                else fileName
            )
            n = int(self.sBox_SampleSize.value())
            if self.chkBox_CustomSeed.isChecked():
                random.seed(int(self.sBox_CustomSeed.value()))
            else:
                random.seed(self.seed)
            
            if self.cBox_SampleType.currentText() == "Random":
                n_list = random.sample(range(self.df_dataset_sampling.shape[0]), n)
                if self.chkBox_InvertSample.isChecked():
                    n_list = list(set(range(self.df_dataset_sampling.shape[0])) - set(n_list))
                sampled_df = self.df_dataset_sampling.iloc[n_list]
            elif self.cBox_SampleType.currentText() == "Ordered":
                n_list = list(range(n))
                if self.chkBox_InvertSample.isChecked():
                    n_list = list(range(n, self.df_dataset_sampling.shape[0]))
                sampled_df = self.df_dataset_sampling.iloc[n_list]
            elif self.cBox_SampleType.currentText() == "Stratified":
                random_seed = (
                    int(self.sBox_CustomSeed.value())
                    if self.chkBox_CustomSeed.isChecked()
                    else self.seed
                )
                sampled_df = self.stratifiedSampling(
                    self.df_dataset_sampling,
                    self.cBox_StratifiedReference.currentText(),
                    n,
                    random_seed,
                )
            sampled_df.to_csv(fileName, index=False)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File saved successfully!")
            msg.setWindowTitle("File saved")
            msg.exec_()

    def btn_LoadDatasetSampling_clicked(self):
        """clicked event on btn_LoadDatasetSampling
        Opens a file dialog to load dataset, csv supported.
        """
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            widget,
            "Open Dataset File",
            "",
            "CSV Files (*.csv)",
            options=options,
        )
        if fileName:
            self.loadDatasetSampling(fileName)

    def stratifiedSampling(self, df, cName, n, random_state=0):
        """Performs stratified sampling on dataset.
        Args:
            df (pd.DataFrame): Pandas dataframe containing all values.
            cName (str): Name of stratified sampling reference column.
            n (float): Sampling percentage.
            random_state (int, optional): Seed to set on RNGs. Defaults to 0.
        Returns:
            pd.DataFrame: Stratified sampling as a pandas DataFrame.
        """
        df_ = df.groupby(cName).apply(
            lambda x: x.sample(
                frac=n * 1.0 / df.shape[0], random_state=random_state
            )
        )
        df_.index = df_.index.droplevel(0)
        if self.chkBox_InvertSample.isChecked():
            new_idx = list(
                set([i for i in range(df.shape[0])]) - set(df_.index.values)
            )
            df_ = df.iloc[new_idx]
        return df_

    def loadDatasetSampling(self, filepath):
        """Loads a dataset in csv format.
        Args:
            filepath (str): File path to the dataset.
        """
        self.txtB_DatasetPathSampling.setText(filepath)

        self.dataset_type = os.path.splitext(filepath)[1][1:].lower()

        if self.dataset_type == "csv":
            self.df_dataset_sampling = pd.read_csv(filepath)

            self.txtB_InfoSamples.setText(
                "{}".format(self.df_dataset_sampling.shape[0])
            )

            self.sBox_SampleSize.setEnabled(False)
            self.dsBox_SamplePerc.setEnabled(True)

            self.rBtn_Size.setChecked(False)
            self.rBtn_SizePerc.setChecked(True)

            self.cBox_SampleType.setEnabled(True)
            self.btn_SaveSample.setEnabled(True)

            self.sBox_handle = "pct"
            self.dsBox_SamplePerc.setValue(0.00)
            self.dsBox_SamplePerc.setValue(10.00)

            sample_type = self.cBox_SampleType.currentText()
            if (
                sample_type == "Stratified"
                and self.df_dataset_sampling is not None
            ):
                self.cBox_StratifiedReference.clear()
                self.cBox_StratifiedReference.addItems(
                    self.df_dataset_sampling.columns.tolist()
                )
                self.cBox_StratifiedReference.setEnabled(True)

    def btn_LoadDatasetLabeling_clicked(self):
        """clicked event on btn_LoadDatasetLabeling
        Opens a file dialog to load dataset, csv supported."""
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            widget,
            "Open Dataset File",
            "",
            "CSV Files (*.csv)",
            options=options,
        )
        if fileName:
            self.loadDatasetLabeling(fileName)

    def loadDatasetLabeling(self, filepath):
        """Loads a dataset in csv format.
        Args:
            filepath (str): File path to the dataset.
        """
        
        self.dataset_labeling_type = os.path.splitext(filepath)[1][1:].lower()

        if self.dataset_labeling_type == "csv":
            self.txtB_DatasetPathLabeling.setText(filepath)
            self.df_dataset_labeling = pd.read_csv(filepath, keep_default_na=False)
            if "risk_level" not in self.df_dataset_labeling.columns:
                self.df_dataset_labeling["risk_level"] = ""
            # if "risk_details" not in self.df_dataset_labeling.columns:
            #     self.df_dataset_labeling["risk_details"] = "{}"

            self.n_samples_labeling = self.df_dataset_labeling.shape[0]
            self.labels = [-1 for _ in range(self.n_samples_labeling)]

            self.txtB_TrueLabel.setText("True Positive")
            self.txtB_TrueLabel.setEnabled(True)
            self.txtB_FalseLabel.setText("False Positive")
            self.txtB_FalseLabel.setEnabled(True)
            self.txtB_ColumnLabel.setText("")
            self.txtB_ColumnLabel.setText("output")
            self.txtB_ColumnLabel.setEnabled(True)

            self.rBtn_CurrentTrue.setEnabled(True)
            self.rBtn_CurrentFalse.setEnabled(True)

            self.sBox_Sample.setEnabled(True)
            self.sBox_Sample.setMaximum(self.n_samples_labeling)
            self.sBox_Sample.setMinimum(1)
            # self.sBox_Sample.setValue(2) # to trigger valueChanged event
            self.sBox_Sample.setValue(1)

            self.btn_PrevLabeling.setEnabled(True)
            self.btn_NextLabeling.setEnabled(True)
            self.btn_SaveDatasetLabeling.setEnabled(True)
            self.btn_Risk.setEnabled(True)

            self.numPages = int(self.n_samples_labeling/25)+1
            self.lbl_PageMaxNumber.setText("/{}".format(self.numPages))
            self.sBox_Page.setMaximum(self.numPages)
            self.sBox_Page.setMinimum(1)
            self.sBox_Page.setValue(1)
            self.sBox_Page.setEnabled(True)
            self.updatePageSamples()
            self.showExampleInTable(0)
        else:
            self.sBox_Page.setEnabled(False)

    def sBox_Page_valueChanged(self):
        self.updatePageSamples()
    
    def updatePageSamples(self):
        if self.sBox_Page.value() == self.numPages:
            for i in range(25 - self.n_samples_labeling % 25):
                self.btns_Page[-i-1].setText("")
                self.btns_Page[-i-1].setEnabled(False)
                self.btns_Page[-i-1].setStyleSheet("background-color: gray; color: black;")
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
            if self.labels[(currPage-1)*25+i] == 1:
                if self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"].lower() == "none":
                    self.btns_Page[i].setStyleSheet("background-color: palegreen;")
                elif self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"].lower() == "low":
                    self.btns_Page[i].setStyleSheet("background-color: khaki;")
                elif self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"].lower() == "medium":
                    self.btns_Page[i].setStyleSheet("background-color: orange;")
                elif self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"].lower() == "high":
                    self.btns_Page[i].setStyleSheet("background-color: orangered;")
                elif self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"].lower() == "critical":
                    self.btns_Page[i].setStyleSheet("background-color: red;")
                else:
                    self.btns_Page[i].setStyleSheet("background-color: white;")
            elif self.labels[(currPage-1)*25+i] == 0:
                self.btns_Page[i].setStyleSheet("background-color: silver;")
            else:
                self.btns_Page[i].setStyleSheet("background-color: white;")

            if self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"] != "" and self.labels[(currPage-1)*25+i] != -1:
                self.btns_Page[i].setText("LR")
            elif self.df_dataset_labeling.iloc[(currPage-1)*25+i]["risk_level"]:
                self.btns_Page[i].setText("R")
            elif self.labels[(currPage-1)*25+i] != -1:
                self.btns_Page[i].setText("L")

            else:
                self.btns_Page[i].setText("")

    def chkBox_CustomSeed_toggled(self):
        """toggled event on chkBox_CustomSeed
        Enables/disables spin box for custom seed value
        """
        if self.chkBox_CustomSeed.isChecked():
            self.sBox_CustomSeed.setEnabled(True)
        else:
            self.sBox_CustomSeed.setEnabled(False)

    def btn_PrevLabeling_clicked(self):
        """clicked event on btn_PrevLabeling
        Sets previous data sample as current if valid.
        """
        curr = int(self.sBox_Sample.value())
        currPage = int(self.sBox_Page.value())
        if curr - 1 > 0:
            self.sBox_Sample.setValue(curr - 1)
            newPage = int(math.ceil((curr - 1)/25))
            if newPage != currPage:
                self.sBox_Page.setValue(newPage)

    def btn_NextLabeling_clicked(self):
        """clicked event on btn_NextLabeling
        Sets next data sample as current if valid.
        """
        curr = int(self.sBox_Sample.value())
        currPage = int(self.sBox_Page.value())
        if curr + 1 <= self.n_samples_labeling:
            self.sBox_Sample.setValue(curr + 1)
            newPage = int(math.ceil((curr + 1)/25))
            if newPage != currPage:
                self.sBox_Page.setValue(newPage)

    def btn_SaveDatasetLabeling_clicked(self):
        """clicked event on btn_SaveDatasetLabeling
        Saves current labeled samples to a new csv file.
        """
        if (
            self.txtB_ColumnLabel.text().strip() != ""
            and self.txtB_TrueLabel.text().strip() != ""
            and self.txtB_FalseLabel.text().strip() != ""
        ):
            widget = QWidget()
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(
                widget,
                "Save Labeled Dataset File",
                "",
                "CSV Files (*.csv)",
                options=options,
            )
            if fileName:
                fileName = (
                    fileName + ".csv"
                    if not fileName.endswith(".csv")
                    else fileName
                )
                true_label_text = self.txtB_TrueLabel.text().strip()
                false_label_text = self.txtB_FalseLabel.text().strip()
                column_label_text = self.txtB_ColumnLabel.text().strip()

                for i, label_val in enumerate(self.labels):
                    if label_val == 0:
                        self.labels[i] = false_label_text
                    elif label_val == 1:
                        self.labels[i] = true_label_text
                    else:
                        self.labels[i] = ""

                self.df_dataset_labeling[column_label_text] = self.labels

                self.df_dataset_labeling.to_csv(fileName, index=False)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(
                    "Labeled dataset file at: {} saved successfully!".format(
                        fileName
                    )
                )
                msg.setWindowTitle("File saved")
                msg.exec_()

    def rBtn_CurrentTrue_toggled(self):
        """toggled event on rBtn_CurrentTrue
        Sets label of current data sample to True"""
        if self.rBtn_CurrentTrue.isChecked():
            self.currentLabel = True
            idx = int(self.sBox_Sample.value()) - 1
            self.labels[idx] = 1
            self.showExampleInTable(idx)
            self.updatePageSamples()

    def rBtn_CurrentFalse_toggled(self):
        """toggled event on rBtn_CurrentFalse
        Sets label of current data sample to False"""
        if self.rBtn_CurrentFalse.isChecked():
            self.currentLabel = False
            idx = int(self.sBox_Sample.value()) - 1
            self.labels[idx] = 0
            self.showExampleInTable(idx)
            self.updatePageSamples()

    def sBox_Sample_valueChanged(self):
        """valueChanged event on sBox_Sample
        Loads a new data sample if value is valid.
        """
        idx = int(self.sBox_Sample.value()) - 1
        if self.labels[idx] == -1:
            self.labels[idx] = 1 if self.currentLabel else 0
        else:
            if self.labels[idx] == 1:
                self.rBtn_CurrentTrue.setChecked(True)
                self.rBtn_CurrentFalse.setChecked(False)
                self.currentLabel = True
            elif self.labels[idx] == 0:
                self.rBtn_CurrentTrue.setChecked(False)
                self.rBtn_CurrentFalse.setChecked(True)
                self.currentLabel = False
        self.displayProgress()
        self.showExampleInTable(idx)
        self.updatePageSamples()

    def txtB_ColumnLabel_textChanged(self):
        """textChanged event on txtB_ColumnLabel
        Checks if output column name exists in current dataset.
        If it exists, checks and loads the column values as labels.
        """
        col_label = self.txtB_ColumnLabel.text().strip()
        if col_label in self.df_dataset_labeling.columns.tolist():
            true_label = self.txtB_TrueLabel.text().lower().strip()
            false_label = self.txtB_FalseLabel.text().lower().strip()

            curr_labels = (
                self.df_dataset_labeling[col_label].astype(str).values.tolist()
            )

            for i, label in enumerate(curr_labels):
                if label.lower().strip() == true_label:
                    self.labels[i] = 1
                elif label.lower().strip() == false_label:
                    self.labels[i] = 0
                else:
                    self.labels[i] = -1

            self.sBox_Sample.setValue(1)

    def displayProgress(self):
        """Displays labeling progress."""
        n_labeled = self.n_samples_labeling - self.labels.count(-1)
        self.lbl_Progress.setText(
            "Progress: {}/{}".format(n_labeled, self.n_samples_labeling)
        )
        self.lbl_ProgressPerc.setText(
            "({:.2f} %)".format(100.0 * n_labeled / self.n_samples_labeling)
        )

    def showExampleInTable(self, idx):
        """Displays sample at specified index from data samples
        Args:
            idx (int): Integer idx of data sample.
        """
        self.tbl_CurrentExample.clearContents()
        self.tbl_CurrentExample.setRowCount(0)
        cols = self.df_dataset_labeling.columns.tolist()
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
                    str(self.df_dataset_labeling[col].iloc[idx])
                ),
            )
        new_row_idx = self.tbl_CurrentExample.rowCount()
        self.tbl_CurrentExample.insertRow(new_row_idx)

        self.tbl_CurrentExample.setItem(
            new_row_idx,
            0,
            QtWidgets.QTableWidgetItem(
                "~{}~".format(self.txtB_ColumnLabel.text().strip())
            ),
        )
        self.tbl_CurrentExample.setItem(
            new_row_idx, 1, QtWidgets.QTableWidgetItem(str(self.currentLabel))
        )

        self.tbl_CurrentExample.resizeRowsToContents()
        
    def home_button_clicked(self):
        from menu import Impl_MainWindow
        self.hm_ui = Impl_MainWindow()
        self.hm_ui.show()
        self.close()
        
    def go_back_button_clicked(self):
        from datasets import Impl_DatasetsWindow
        self.hm_ui = Impl_DatasetsWindow()
        self.hm_ui.show()
        self.close()
