import csv
import datetime
import json

import numpy as np
from dataset_column import DatasetColumn
from vinci_utils import(
    CODE_DX_PRESET_XML,
    CODE_DX_PRESET_CSV,
    PMD_PRESET_CSV,
    PMD_PRESET_XML,
    PMD_PRESET_JSON,
    #CODE_DX_PRESET_CSV_DETAILS,
    GENDARME_PRESET_XML,
    SPOTBUGS_PRESET_XML,
    FORTIFY_PRESET_XML,
    CPPCHECK_PRESET_XML,
    PMD_PRESET_ROOT,
    CODE_DX_PRESET_XML_ROOT,
    GENDARME_PRESET_XML_ROOT,
    SPOTBUGS_PRESET_XML_ROOT, 
    FORTIFY_PRESET_XML_ROOT,
    CPPCHECK_PRESET_XML_ROOT,
    PHP_CODESNIFFER_PRESET_ROOT,
    PYLINT_PRESET_JSON,
    PHP_CODESNIFFER_PRESET_CSV,
    PHP_CODESNIFFER_PRESET_JSON,
    JSHINT_PRESET_XML,
    JSHINT_PRESET_JSON,
    PHP_CODESNIFFER_PRESET_XML,
    ESLINT_PRESET_JSON,
)
import pandas as pd
import os
from datasets_ui import Ui_DatasetsWindow
from datasets_workers import (
    WorkerLoadXMLDataset,
    WorkerLoadXMLCols,
    WorkerLoadFPRDataset,
    WorkerLoadZIPDataset,
)
from datasets_labeler import Impl_DatasetsLabelerWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from help import Impl_HelpWindow
from PyQt5.QtCore import pyqtSignal

class Impl_DatasetsWindow(Ui_DatasetsWindow, QtWidgets.QMainWindow,):
    """Creates menu window"""

    def __init__(self):
        """Initializes datasets window object"""
        super(Impl_DatasetsWindow, self).__init__()
        self.saved_dataset_path = None
        self.xml_tag = None
        self.setupUi(self)

        self.customEvents()
        self.customInit()


    def customInit(self):
        """Custom init method"""
        self.btn_AddColumn.setEnabled(False)
        self.btn_RemoveColumn.setEnabled(False)
        self.btn_SaveSchema.setEnabled(False)
        self.btn_SaveDataset.setEnabled(False)
        self.worker_xml_cols = None
        self.worker_xml_ds = None
        self.worker_xml_schema = None
        self.worker_xml_schema_cols = None

    def customEvents(self):
        """Custom events method; here you connect functions with the UI."""
        self.home_button.triggered.connect(self.home_button_clicked)
        self.go_back_button.triggered.connect(self.home_button_clicked)
        self.btn_LoadDataset.clicked.connect(self.btn_LoadDataset_clicked)
        self.btn_AddColumn.clicked.connect(self.btn_AddColumn_clicked)
        self.btn_RemoveColumn.clicked.connect(self.btn_RemoveColumn_clicked)
        self.btn_SaveDataset.clicked.connect(self.btn_SaveDataset_clicked)
        self.btn_SaveSchema.clicked.connect(self.btn_SaveSchema_clicked)
        self.btn_LoadSchema.clicked.connect(self.btn_LoadSchema_clicked)
        self.btn_Labeler.clicked.connect(self.btn_Labeler_clicked)
        self.btn_Help.clicked.connect(self.btn_Help_clicked)
        self.cBox_Root.currentTextChanged.connect(
            self.cBox_Root_currentTextChanged
        )
        self.cBox_Column.currentTextChanged.connect(
            self.cBox_Column_currentTextChanged
        )
        self.cBox_Data.currentTextChanged.connect(
            self.cBox_Data_currentTextChanged
        )
        self.cBox_Type.currentTextChanged.connect(
            self.cBox_Type_currentTextChanged
        )
        self.cBox_Preset.currentTextChanged.connect(
            self.cBox_Preset_currentTextChanged
        )
        self.hSld_TrainTestSplit.valueChanged.connect(
            self.hSld_TrainTestSplit_valueChanged
        )
    
    def home_button_clicked(self):
        from menu import Impl_MainWindow
        self.hm_ui = Impl_MainWindow()
        self.hm_ui.show()
        self.close()
    
    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
         Loads and show Help Window.
         """
        self.hs_ui = Impl_HelpWindow("Dataset")
        self.hs_ui.show()


    def btn_Labeler_clicked(self):
        """Clicked event on btn_Labeler component."""
        """if dataset is xml and a respective csv file is not already present give user a choice to do so"""
        if self.xml_tag is not None:
           self.btn_SaveDataset_clicked()
        if self.saved_dataset_path is None:
            msg_box = QMessageBox()
            msg_box.setText("Please Save dataset before exporting!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        elif self.saved_dataset_path is not None:
            self.dsl_ui = Impl_DatasetsLabelerWindow(self.saved_dataset_path)
            self.dsl_ui.show()
            self.close()


    def convertXmlToCSV(self, fileName):
        """Clicked event on btn_Labeler component.
        
        Args:
            fileName (str): Filepath to save dataset to.
        """

        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        csvFilename, _ = QFileDialog.getSaveFileName(
            widget,
            "Save Sampled CSV File",
            "",
            "CSV File (*.csv)",
            options=options,
        )
        csvFilename = csvFilename + ".csv"
        self.saveCsvDatasetFile(csvFilename)
        return csvFilename

    def saveCsvDatasetFile(self, fileName):
        """Saves dataset as CSV. Useful to extract XML data into a CSV file

        Args:
            fileName (str): Filepath to save dataset to.
        """
        self.d = self.ds_xml_dict.copy()
        for k in self.ds_roots[self.cBox_Root.currentIndex()]:
            self.d = self.d[k]

        print()
        cols = [col.split_name_xml() for col in self.datasetColumns]

        self.df_dataset = self.createDataFrameFromXML(self.d, cols)

        self.df_dataset.to_csv(fileName, index=False)

    def checkFileFormat(self, fileName):
        """Check if the file the format is xml or not"""
        if fileName.endswith(".xml"):
            return True
        return False

    def saveDatasetFile(self, fileName):
        """Saves dataset as CSV. Useful to extract XML data into a CSV file

        Args:
            fileName (str): Filepath to save dataset to.
        """
        self.d = self.ds_xml_dict.copy()
        try:
         for k in self.ds_roots[self.cBox_Root.currentIndex()]:
             self.d = self.d[k]
        except IndexError:
            print("Error: Index is out of bounds.")
        cols = [col.split_name_xml() for col in self.datasetColumns]
        self.df_dataset = self.createDataFrameFromXML(self.d, cols)

        #self.df_dataset = self.df_dataset.drop_duplicates()

        self.df_dataset.to_csv(fileName, index=False)
        self.saved_dataset_path = fileName

    def btn_SaveDataset_clicked(self):
        """clicked event on btn_SaveDataset

        Opens a SaveFileDialog to specify the path to save as new dataset.
        """
        if self.xml_tag is not None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            fileName = os.path.splitext(os.path.basename(self.saved_dataset_path))[0]+"_"+str(timestamp)+ ".csv"
            self.saveDatasetFile(fileName)
        elif self.tbl_Dataset.rowCount() > 0:
            widget = QWidget()
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(
                widget,
                "Save as new Dataset File",
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
                self.saveDatasetFile(fileName)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("No columns")
            msg.setText("You must have at least 1 column added!")
            msg.exec_()

    def btn_LoadDataset_clicked(self):
        """Opens a file dialog to load dataset."""
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            widget,
            "Open Dataset File",
            "",
            "All supported files (*.csv *.xml *.fpr *.zip *.json);;"
            + " CSV Files (*.csv);;"
            + " XML files (*.xml);;"
            + " Fortify Files (*.fpr);;"
            + " Pylint Files (*.json)"
            + " CppCheck Files (*.zip)",
            options=options,
        )
        if fileName:
            self.loadDatasetFile(fileName)
        return fileName

    def evtWorkerLoadXMLDataset(self, params):
        """Thread method to load xml dataset.

        Args:
            params (dict): Parameters ds_xml_dict, ds_roots
        """
        self.ds_xml_dict = params["ds_xml_dict"]

        self.ds_roots = params["ds_roots"]

        self.ds_raw = params["ds_raw"]

        self.cBox_Column.clear()

        roots = ["->".join(r) for r in self.ds_roots]

        if len(self.ds_roots) > 0:
            self.cBox_Root.clear()
            self.cBox_Root.addItems(roots)
            self.cBox_Root.setEnabled(True)

        trainSplit = self.hSld_TrainTestSplit.value()
        self.txtB_TrainPercentage.setText("{0}".format(trainSplit))
        self.txtB_TestPercentage.setText("{0}".format(100 - trainSplit))

        self.cBox_Data.clear()
        #self.cBox_Data.addItems(["Categorical", "Numerical"])
        self.cBox_Data.addItems(["Categorical"])

        self.cBox_Training.clear()
        self.cBox_Training.addItems(["Yes", "No"])

        self.cBox_Type.clear()
        self.cBox_Type.addItems(["Input", "Output"])

        self.tbl_Dataset.clearContents()
        self.tbl_Dataset.setRowCount(0)
        self.datasetColumns = []
        self.btn_AddColumn.setEnabled(True)
        self.btn_RemoveColumn.setEnabled(True)
        self.btn_SaveSchema.setEnabled(True)
        self.btn_SaveDataset.setEnabled(True)

        self.inferDatasetOriginTool()

        self.statusBar().showMessage("Loading XML Dataset Done!", 3000)
        self.d = self.ds_xml_dict.copy()
        try:
         for k in self.ds_roots[self.cBox_Root.currentIndex()]:
             self.d = self.d[k]
        except IndexError:
            print("Error: Index is out of bounds.")
        cols = [col.split_name_xml() for col in self.datasetColumns]
        self.df_dataset = self.createDataFrameFromXML(self.d, cols)
        self.cBox_Column.addItems(list(self.df_dataset.columns))

    def inferDatasetOriginToolforCsv(self):
        # Current ds should be an XML
        print("coming into inferdatasetoriginal csv tool")
        self.ds_raw = str(self.ds_raw)
        origin_idx = -1
        origin_str = None
       
        if '@status' in self.ds_raw:
            # Current dataset comes from CodeDx CSV
            origin_idx = 2
            origin_str = "CodeDx"
        elif "Package" in self.ds_raw:
            # Current dataset comes from PMD CSV
            origin_idx = 3
            origin_str = "PMD"
        elif "Fixable" in self.ds_raw:
            # Current dataset comes from PHP CSV
            origin_idx = 12
            origin_str = "PHP"
        if origin_idx != -1:
            QMessageBox.information(
                self,
                "Autoload Preset",
                "Preset for {} has been loaded.\nYou can add/remove features as you see fit.".format(
                    origin_str
                ),
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            self.cBox_Preset.setCurrentIndex(origin_idx)
            self.btn_SaveDataset.setEnabled(False)
    
    def inferDatasetOriginToolforJSON(self):
        # Current ds should be an JSON
        print("coming into inferdatasetoriginal json tool")
        with open(self.txtB_DatasetPath.text()) as f:
            jsondata = json.load(f)
        origin_idx = -1
        origin_str = None
        if 'messages' in jsondata:
            # Current dataset comes from CodeDx CSV
            origin_idx = 17
            origin_str = "ESLint"
        elif 'result' in jsondata:
            origin_idx = 16
            origin_str = "JSHint"
        elif 'files' in jsondata:
            origin_idx = 14
            origin_str = "PHP_CodeSniffer"
        if origin_idx != -1:
            QMessageBox.information(
                self,
                "Autoload Preset",
                "Preset for {} has been loaded.\nYou can add/remove features as you see fit.".format(
                    origin_str
                ),
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            self.cBox_Preset.setCurrentIndex(origin_idx)
            self.btn_SaveDataset.setEnabled(False)
        
    def inferDatasetOriginTool(self):
        # Current ds should be an XML
        print("coming into inferdatasetoriginal tool")
        self.ds_raw = str(self.ds_raw)
        origin_idx = -1
        origin_str = None

        if 'generator="codedx"' in self.ds_raw:
            # Current dataset comes from CodeDx XML
            origin_idx = 1
            origin_str = "CodeDx"
        elif "gendarme-output" in self.ds_raw:
            # Current dataset comes from Gendarme XML
            origin_idx = 6
            origin_str = "Gendarme"
        elif "<BugCollection" in self.ds_raw or "<BugInstance" in self.ds_raw:
            # Current dataset comes from SpotBugs
            #origin_idx = 5 fails using the preset
            origin_idx = 7
            origin_str = "SpotBugs"
        elif (
            '<FVDL xmlns="xmlns://www.fortifysoftware.com/schema/fvdl"'
            in self.ds_raw
        ):
            # Current dataset comes from Fortify
            origin_idx = 8
            origin_str = "Fortify"
        elif "<cppcheck" in self.ds_raw:
            # Current dataset comes from CppCheck
            origin_idx = 9
            origin_str = "CppCheck"
        elif "<pmd" in self.ds_raw:
            # Current dataset comes from PMD
            origin_idx = 4
            origin_str = "PMD"
        elif "<checkstyle" in self.ds_raw:
            # Current dataset comes from JSHint
            origin_idx = 15
            origin_str = "JSHint"
        elif "<phpcs" in self.ds_raw:
            # Current dataset comes from PHOCodeSniffer
            origin_idx = 13
            origin_str = "PHP_CodeSniffer"
        if origin_idx != -1:
            QMessageBox.information(
                self,
                "Autoload Preset",
                "Preset for {} has been loaded.\nYou can add/remove features as you see fit.".format(
                    origin_str
                ),
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            self.cBox_Preset.setCurrentIndex(origin_idx)
            self.btn_SaveDataset.setEnabled(False)

    def loadDatasetFile(self, filepath, reportType=None):
        """Loads a datasets either in csv or xml format.

        Args:
            filepath (str): File path to the dataset.
        """
        if os.path.getsize(filepath) == 0:
            QMessageBox.warning(self, 'Empty Dataset', 'The selected dataset file is empty. Reload another file.',
                            QMessageBox.Ok)
            return
        self.txtB_DatasetPath.setText(filepath)
        self.dataset_type = os.path.splitext(filepath)[1][1:].lower()

        self.cBox_Preset.clear()
        self.cBox_Preset.addItems(
            [
                "Custom",
                "CodeDx (XML)",
                "CodeDx (CSV)",
                "PMD (CSV)",
                "PMD (XML)",
                "PMD (JSON)",
                #"CodeDx (CSV w/Details)",
                "Gendarme (XML)",
               "SpotBugs (XML)",
                "Fortify (FPR)",
                "CppCheck (XML)",
                "SonarQube (XML)",
                "Pylint (JSON)",
                "PHP_CodeSniffer(CSV)",
                "PHP_CodeSniffer(XML)",
                "PHP_CodeSniffer(JSON)",
                "JSHint (XML)",
                "JSHint (JSON)",
                "ESLint (JSON)",
            ]
        )
        self.cBox_Preset.setEnabled(True)

        if self.dataset_type == "csv":
            self.saved_dataset_path = filepath
            self.df_dataset = pd.read_csv(filepath)

            if 'Fixable' in self.df_dataset and 'Status' not in self.df_dataset:
                self.df_dataset['Status'] = self.df_dataset['Fixable']
                first_column = self.df_dataset.pop('Status')
                self.df_dataset.insert(0,'Status',first_column)
                print(self.df_dataset.columns)
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(0, 'false-positive')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(1, 'escalated')

            if 'Priority' in self.df_dataset and 'Status' not in self.df_dataset:
                self.df_dataset['Status'] = self.df_dataset['Priority']
                first_column = self.df_dataset.pop('Status')
                self.df_dataset.insert(0,'Status',first_column)
                # self.df_dataset['Status'] = np.where(self.df_dataset['Status']>=3,'escalated','false-positive')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(0, 'false-positive')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(1, 'false-positive')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(2, 'false-positive')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(3, 'escalated')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(4, 'escalated')
                self.df_dataset['Status'] = self.df_dataset['Status'].replace(5, 'escalated')
                
            print(type(self.df_dataset))
            print(self.df_dataset)
            self.df_dataset.to_csv(filepath,mode = 'w', index=False)

            self.ds_xml_dict = {}

            with open(filepath, "r", encoding="utf-8") as f:
                self.ds_raw = f.read()
           
            self.txtB_InfoSamples.setText(
                "{}".format(self.df_dataset.shape[0])
            )
            self.txtB_InfoFeatures.setText(
                "{}".format(self.df_dataset.shape[1])
            )

            trainSplit = self.hSld_TrainTestSplit.value()
            self.txtB_TrainPercentage.setText("{0}".format(trainSplit))
            self.txtB_TestPercentage.setText("{0}".format(100 - trainSplit))

            self.ds_roots = []

            self.cBox_Root.clear()

            self.cBox_Column.clear()
            self.cBox_Column.addItems(list(self.df_dataset.columns))

            self.cBox_Data.clear()
            #self.cBox_Data.addItems(["Categorical", "Numerical"])
            self.cBox_Data.addItems(["Categorical"])

            self.cBox_Training.clear()
            self.cBox_Training.addItems(["Yes", "No"])

            self.cBox_Type.clear()
            self.cBox_Type.addItems(["Input", "Output"])

            self.tbl_Dataset.clearContents()
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.btn_AddColumn.setEnabled(True)
            self.btn_RemoveColumn.setEnabled(True)
            self.btn_SaveSchema.setEnabled(True)
            self.btn_SaveDataset.setEnabled(True)
            self.cBox_Root.setEnabled(False)
            self.inferDatasetOriginToolforCsv()

        elif self.dataset_type == "xml":
            self.ds_xml_dict = {}
            self.xml_tag = True
            self.saved_dataset_path = filepath
            self.statusBar().showMessage("Loading XML Dataset, please wait...")

            self.worker_xml_ds = WorkerLoadXMLDataset(filepath, parent=self)
            self.worker_xml_ds.start()
            self.worker_xml_ds.worker_complete.connect(
                self.evtWorkerLoadXMLDataset
            )
        elif self.dataset_type == "fpr":
            self.ds_xml_dict = {}
            self.saved_dataset_path = None

            self.statusBar().showMessage("Loading FPR Dataset, please wait...")

            self.worker_xml_ds = WorkerLoadFPRDataset(filepath, parent=self)
            self.worker_xml_ds.start()
            self.worker_xml_ds.worker_complete.connect(
                self.evtWorkerLoadXMLDataset
            )
        elif self.dataset_type == "zip":
            self.ds_xml_dict = {}
            self.saved_dataset_path = None

            self.statusBar().showMessage("Loading ZIP Dataset, please wait...")

            self.worker_xml_ds = WorkerLoadZIPDataset(filepath, parent=self)
            self.worker_xml_ds.start()
            self.worker_xml_ds.worker_complete.connect(
                self.evtWorkerLoadXMLDataset
            )
        elif self.dataset_type == "json":
            self.statusBar().showMessage("JSON file loaded, Please select preset")
            self.cBox_Root.clear()
            self.cBox_Column.clear()
            self.cBox_Data.clear()
            self.cBox_Type.clear()
            self.cBox_Transformation.clear()
            self.cBox_TPLabel.clear()
            self.cBox_Training.clear()
            self.tbl_Dataset.clearContents()
            self.tbl_Dataset.setRowCount(0)
            self.btn_AddColumn.setEnabled(False)
            self.btn_RemoveColumn.setEnabled(False)
            self.btn_SaveSchema.setEnabled(False)
            self.btn_SaveDataset.setEnabled(False)
            self.cBox_Root.setEnabled(False)
            self.inferDatasetOriginToolforJSON()

    def btn_LoadSchema_clicked(self):
        """Clicked event on btn_LoadSchema
        Opens a FileDialog to load an schema.
        """
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            widget,
            "Open Schema File",
            "",
            "JSON Files (*.json)",
            options=options,
        )
        if fileName:
            self.loadSchemaFile(fileName)

    def evtWorkerLoadXMLSchemaCols(self, params):
        """Thread method to load columns of an xml schema.

        Args:
            params (dict): Contains ds_cols
        """
        self.ds_cols = params["ds_cols"]
        self.df_dataset = self.createDataFrameFromXML(self.d, self.ds_cols)
        self.txtB_InfoSamples.setText("{}".format(self.df_dataset.shape[0]))
        self.txtB_InfoFeatures.setText("{}".format(self.df_dataset.shape[1]))

        self.hSld_TrainTestSplit.setValue(
            int(self.schemaContent["trainSplit"])
        )
        self.txtB_TrainPercentage.setText(
            "{0}".format(int(self.schemaContent["trainSplit"]))
        )
        self.txtB_TestPercentage.setText(
            "{0}".format(100 - int(self.schemaContent["trainSplit"]))
        )

        self.cBox_Column.clear()
        self.cBox_Column.addItems(list(self.df_dataset.columns))

        self.cBox_Data.clear()
        #self.cBox_Data.addItems(["Categorical", "Numerical"])
        self.cBox_Data.addItems(["Categorical"])

        self.cBox_Training.clear()
        self.cBox_Training.addItems(["Yes", "No"])

        self.cBox_Type.clear()
        self.cBox_Type.addItems(["Input", "Output"])

        self.tbl_Dataset.clearContents()
        self.tbl_Dataset.setRowCount(0)
        self.datasetColumns = []
        self.btn_AddColumn.setEnabled(True)
        self.btn_RemoveColumn.setEnabled(True)
        self.btn_SaveSchema.setEnabled(True)

        for c in self.schemaContent["columns"]:
            dsCol = DatasetColumn.fromdict(c)
            self.datasetColumns.append(dsCol)
            new_row_idx = self.tbl_Dataset.rowCount()

            self.tbl_Dataset.insertRow(new_row_idx)

            self.tbl_Dataset.setItem(
                new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
            )
            self.tbl_Dataset.setItem(
                new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
            )
            self.tbl_Dataset.setItem(
                new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
            )
            self.tbl_Dataset.setItem(
                new_row_idx,
                3,
                QtWidgets.QTableWidgetItem(dsCol.Transformation),
            )
            self.tbl_Dataset.setItem(
                new_row_idx,
                4,
                QtWidgets.QTableWidgetItem(
                    dsCol.Type
                    if dsCol.TPLabel == ""
                    else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                ),
            )
        self.statusBar().showMessage("Loading XML Schema, Done!", 3000)

    def evtWorkerLoadXMLSchema(self, params):
        """Thread method to load an xml schema

        Args:
            params (dict): Contains ds_xml_dict, ds_roots
        """
        self.ds_xml_dict = params["ds_xml_dict"]
        self.ds_roots = params["ds_roots"]
        if len(self.ds_roots) > 0:
            self.cBox_Root.clear()
            roots = ["->".join(r) for r in self.ds_roots]
            self.cBox_Root.addItems(roots)
            self.cBox_Root.setEnabled(True)
        selectedRoot = self.schemaContent["xml_params"]["root"]
        self.d = self.ds_xml_dict.copy()
        for c in selectedRoot:
            self.d = self.d[c]

        self.worker_xml_schema_cols = WorkerLoadXMLCols(self.d, parent=self)
        self.worker_xml_schema_cols.start()
        self.worker_xml_schema_cols.worker_complete.connect(
            self.evtWorkerLoadXMLSchemaCols
        )

    def loadSchemaFile(self, filename):
        """Loads and schema files

        Args:
            filename (str): Filepath to the schema file
        """
        with open(filename, "r", encoding="utf-8") as fp:
            self.schemaContent = json.load(fp)
        is_ok, msgStr = self.checkSchemaFileHealth(self.schemaContent)
        if not is_ok:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Schema file corrupted!")
            msg.setText(msgStr)
            msg.exec_()
            return

        self.txtB_DatasetPath.setText(self.schemaContent["filename"])
        self.dataset_type = self.schemaContent["format"]
        if self.schemaContent["format"] == "csv":
            try:
                self.df_dataset = pd.read_csv(self.schemaContent["filename"])
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Filename not working!")
                msg.setText("File at {} does not exist or is corrupted. Please check!".format(self.schemaContent["filename"]))
                msg.exec_()
            self.txtB_InfoSamples.setText(
                "{}".format(self.df_dataset.shape[0])
            )
            self.txtB_InfoFeatures.setText(
                "{}".format(self.df_dataset.shape[1])
            )

            self.hSld_TrainTestSplit.setValue(
                int(self.schemaContent["trainSplit"])
            )
            self.txtB_TrainPercentage.setText(
                "{0}".format(int(self.schemaContent["trainSplit"]))
            )
            self.txtB_TestPercentage.setText(
                "{0}".format(100 - int(self.schemaContent["trainSplit"]))
            )

            self.cBox_Column.clear()
            self.cBox_Column.addItems(list(self.df_dataset.columns))

            self.cBox_Data.clear()
            #self.cBox_Data.addItems(["Categorical", "Numerical"])
            self.cBox_Data.addItems(["Categorical"])

            self.cBox_Training.clear()
            self.cBox_Training.addItems(["Yes", "No"])

            self.cBox_Type.clear()
            self.cBox_Type.addItems(["Input", "Output"])

            self.tbl_Dataset.clearContents()
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.btn_AddColumn.setEnabled(True)
            self.btn_RemoveColumn.setEnabled(True)
            self.btn_SaveSchema.setEnabled(True)

            for c in self.schemaContent["columns"]:
                dsCol = DatasetColumn.fromdict(c)
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif self.schemaContent["format"] == "xml":
            self.statusBar().showMessage("Loading XML Schema, please wait...")
            self.worker_xml_schema = WorkerLoadXMLDataset(
                self.schemaContent["filename"], parent=self
            )
            self.worker_xml_schema.start()
            self.worker_xml_schema.worker_complete.connect(
                self.evtWorkerLoadXMLSchema
            )

    def checkSchemaFileHealth(self, json_dict):
        """Checks for sanity of schema file by checking all keys exist.txt

        Args:
            json_dict (dict): Dict with all params of

        Returns:
            tuple(bool,str): Tuple containing check passed and error if exists.
        """
        if "filename" not in json_dict:
            return False, "Filename not found on schema file."
        if "columns" not in json_dict:
            return False, "Columns not found on schema file."
        if "format" not in json_dict:
            return False, "Format not found on schema file."
        if "xml_params" not in json_dict:
            return False, "XML params not found on schema file."
        if "trainSplit" not in json_dict:
            return False, "Train split value not found on schema file."
        if "testSplit" not in json_dict:
            return False, "Test split value not found on schema file."
        if "trainIdx" not in json_dict:
            return False, "Train index not found on schema file."
        if "testIdx" not in json_dict:
            return False, "Test index not found on schema file."
        return True, ""

    def createDataFrameFromXML(self, dict_list, ds_cols):
        """Creates a pandas dataframe from an xml file

        Args:
            dict_list (list(dict)): List of dictionaries extracted from XML file
            ds_cols (list): List of dataset columns

        Returns:
            pd.DataFrame: Pandas dataframe containing all data
        """
    
        col_data = [[] for _ in range(len(ds_cols))]
        items = dict_list
        if self.cBox_Preset.currentText() == "CodeDx (XML)":
         items = dict_list['report']['findings']['finding']
        elif self.cBox_Preset.currentText() == "JSHint (XML)":
         items = dict_list['checkstyle']['file']['error']
        elif self.cBox_Preset.currentText() == "SpotBugs (XML)":
         items = dict_list['BugCollection']['BugInstance']
        elif self.cBox_Preset.currentText() == "CppCheck (XML)":
         items = dict_list['results']['errors']['error']
        elif self.cBox_Preset.currentText() == "Gendarme (XML)":
         items = dict_list['gendarme-output']['results']['rule']
        elif self.cBox_Preset.currentText() == "PHP_CodeSniffer(XML)":
         items = dict_list['phpcs']['file']['error']
        for entry in items:
            for i in range(len(ds_cols)):
                curr_col = ds_cols[i]
                value = entry
                for j in range(len(curr_col)):
                    if (
                        value is None
                        or curr_col[j] not in value
                        or type(curr_col[j]) != str
                    ):
                        value = ""
                        break
                    value = value[curr_col[j]]
                col_data[i].append(value)
        cols = ["->".join(c) for c in ds_cols]

        df_dataset = pd.DataFrame()

        for i in range(len(cols)):
            df_dataset[cols[i]] = col_data[i]

        if '@priority' in df_dataset:
            df_dataset['@status'] = df_dataset['@priority']
            first_column = df_dataset.pop('@status')
            df_dataset.insert(0,'@status',first_column)
            df_dataset['@status'] = np.where(df_dataset['@status']>="3",'escalated','false-positive')
        elif '@Fixable' in df_dataset:
            df_dataset['@status'] = df_dataset['@Fixable']
            first_column = df_dataset.pop('@status')
            df_dataset.insert(0,'@status',first_column)
            df_dataset['@status'] = df_dataset["@status"].replace(0,'false-positive')
            df_dataset['@status'] = df_dataset["@status"].replace(1,'escalated') 

        print("dataset")
        print(df_dataset) 

        return df_dataset

    @pyqtSlot(dict)
    def evtWorkerLoadXMLCols(self, params):
        """Thread method to search for all xml columns

        Args:
            params (dict): Contains ds_cols
        """
        self.ds_cols = params["ds_cols"]

        self.txtB_InfoFeatures.setText("{}".format(len(self.ds_cols)))

        self.txtB_InfoSamples.setText("{}".format(len(self.d)))

        cols = ["output"] + ["->".join(c) for c in self.ds_cols]
        if len(self.ds_cols) > 0:
            self.cBox_Column.clear()
            self.cBox_Column.addItems(cols)
            self.df_dataset = self.createDataFrameFromXML(self.d, self.ds_cols)
            self.txtB_InfoSamples.setText(
                "{}".format(self.df_dataset.shape[0])
            )
            self.txtB_InfoFeatures.setText(
                "{}".format(self.df_dataset.shape[1])
            )
            self.statusBar().showMessage(
                "Loading XML Dataset Columns, Done!", 3000
            )

    def cBox_Root_currentTextChanged(self):
        """currentTextChanged event on cBox_Root
        Starts loading possible columns if xml root changes.
        """
        if self.dataset_type == "xml":
            self.d = self.ds_xml_dict.copy()
            for k in self.ds_roots[self.cBox_Root.currentIndex()]:
                self.d = self.d[k]

            self.cBox_Column.clear()
            self.statusBar().showMessage("Loading XML Dataset Columns...")

            self.worker_xml_cols = WorkerLoadXMLCols(self.d, parent=self)
            self.worker_xml_cols.start()
            self.worker_xml_cols.worker_complete.connect(
                self.evtWorkerLoadXMLCols
            )
        elif self.dataset_type == "fpr":
            self.d = self.ds_xml_dict.copy()
            for k in self.ds_roots[self.cBox_Root.currentIndex()]:
                self.d = self.d[k]

            self.cBox_Column.clear()
            self.statusBar().showMessage("Loading XML Dataset Columns...")

            self.worker_xml_cols = WorkerLoadXMLCols(self.d, parent=self)
            self.worker_xml_cols.start()
            self.worker_xml_cols.worker_complete.connect(
                self.evtWorkerLoadXMLCols
            )
        elif self.dataset_type == "zip":
            self.d = self.ds_xml_dict.copy()
            for k in self.ds_roots[self.cBox_Root.currentIndex()]:
                self.d = self.d[k]

            self.cBox_Column.clear()
            self.statusBar().showMessage("Loading XML Dataset Columns...")

            self.worker_xml_cols = WorkerLoadXMLCols(self.d, parent=self)
            self.worker_xml_cols.start()
            self.worker_xml_cols.worker_complete.connect(
                self.evtWorkerLoadXMLCols
            )

    def cBox_Column_currentTextChanged(self):
        """currentTextChanged event on cBox_Column
        Displays possible columns to be output column.
        """
        if self.cBox_Type.currentText() == "Output":
            self.cBox_TPLabel.clear()
            #if self.cBox_Column.currentText() == "output":
            #    self.cBox_TPLabel.addItems(["True Positive"])
            #else:
            if self.cBox_Column.currentText() != "":
                self.cBox_TPLabel.addItems(
                    self.df_dataset[self.cBox_Column.currentText()]
                    .astype(str)
                    .unique()
                )

    def cBox_Data_currentTextChanged(self):
        """currentTextChanged event on cBox_Data
        Adds possible transformations options depending on data type.
        """
        if self.cBox_Data.currentText() == "Numerical":
            self.cBox_Transformation.clear()
            self.cBox_Transformation.addItems(
                ["Gaussian Dist", "Uniform Dist"]
            )
        elif self.cBox_Data.currentText() == "Categorical":
            self.cBox_Transformation.clear()
            self.cBox_Transformation.addItems(["One-hot Encoding"])

    def cBox_Type_currentTextChanged(self):
        """currentTextChanged event on cBox_Type
        Loads true positive label options if needed.
        """
        self.cBox_TPLabel.clear()
        if self.cBox_Type.currentText() == "Input":
            self.cBox_TPLabel.setEnabled(False)
        elif (
            self.cBox_Type.currentText() == "Output"
            and self.cBox_Column.currentText() != ""
        ):
            self.cBox_TPLabel.setEnabled(True)
            #if self.cBox_Column.currentText() == "output":
            #    self.cBox_TPLabel.addItems(["True Positive"])
            #else:
            if self.cBox_Column.currentText() in self.df_dataset.columns: 
                self.cBox_TPLabel.addItems(
                    self.df_dataset[self.cBox_Column.currentText()]
                    .astype(str)
                    .unique()
                )
# this is where the json file is loaded at the interface
# need to make sure the correct schema is used, each dataset is unique
# adjust
    def cBox_Preset_selected_json(self, preset):
        if self.txtB_DatasetPath.text() is None:
            return
        with open(self.txtB_DatasetPath.text()) as f:
            jsondata = json.load(f)
        with open('data.csv', 'w', newline ='') as f:
            writer = csv.writer(f)
            if preset == "PMD (JSON)" and 'files' in jsondata:
                writer.writerow(PMD_PRESET_JSON)
                if 'violations' in jsondata['files'][0]:
                    for csvdata in jsondata['files'][0]['violations']:
                        data = []
                        for col in PMD_PRESET_JSON:
                            data.append(csvdata[col])
                        writer.writerow(data)
            elif preset == "PHP_CodeSniffer(JSON)" and 'files' in jsondata:
                writer.writerow(PHP_CODESNIFFER_PRESET_JSON)
                for csvdata in jsondata['files']:
                    if 'messages' in csvdata:
                        data = []
                        for col in PHP_CODESNIFFER_PRESET_JSON:
                            data.append(csvdata['messages'][col])
                        writer.writerow(data)
            elif preset == "JSHint (JSON)" and 'result' in jsondata:
                writer.writerow(JSHINT_PRESET_JSON)
                for csvdata in jsondata['result']:
                    if 'error' in csvdata:
                        data = []
                        for col in JSHINT_PRESET_JSON:
                            data.append(csvdata['error'][col])
                        writer.writerow(data)
            elif preset == "ESLint (JSON)" and "messages" in jsondata:
                writer.writerow(ESLINT_PRESET_JSON)
                for csvdata in jsondata['messages']:
                    data = []
                    for col in ESLINT_PRESET_JSON:
                        data.append(csvdata[col])
                    writer.writerow(data)
            elif preset == "Pylint (JSON)":
                writer.writerow(PYLINT_PRESET_JSON)
                for csvdata in jsondata:
                    data = []
                    for col in PYLINT_PRESET_JSON:
                        data.append(csvdata[col])
                    writer.writerow(data)
            else:
                return

        filepath = 'data.csv'
        self.saved_dataset_path = filepath
        self.df_dataset = pd.read_csv(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            self.ds_raw = f.read()

        self.txtB_InfoSamples.setText(
            "{}".format(self.df_dataset.shape[0])
        )
        self.txtB_InfoFeatures.setText(
            "{}".format(self.df_dataset.shape[1])
        )

        trainSplit = self.hSld_TrainTestSplit.value()
        self.txtB_TrainPercentage.setText("{0}".format(trainSplit))
        self.txtB_TestPercentage.setText("{0}".format(100 - trainSplit))

        self.ds_roots = []

        self.cBox_Root.clear()

        self.cBox_Column.clear()
        self.cBox_Column.addItems(list(self.df_dataset.columns))

        self.cBox_Data.clear()
        #self.cBox_Data.addItems(["Categorical", "Numerical"])
        self.cBox_Data.addItems(["Categorical"])

        self.cBox_Training.clear()
        self.cBox_Training.addItems(["Yes", "No"])

        self.cBox_Type.clear()
        self.cBox_Type.addItems(["Input", "Output"])

        self.tbl_Dataset.clearContents()
        self.tbl_Dataset.setRowCount(0)
        self.datasetColumns = []
        self.btn_AddColumn.setEnabled(True)
        self.btn_RemoveColumn.setEnabled(True)
        self.btn_SaveSchema.setEnabled(True)
        self.btn_SaveDataset.setEnabled(True)

    def cBox_Preset_currentTextChanged(self):
        """currentTextChanged event on cBox_Preset
        Populates our column table with selected preset.
        """
        currText = self.cBox_Preset.currentText()
        if currText == "CodeDx (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == CODE_DX_PRESET_XML_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(CODE_DX_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        CODE_DX_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        CODE_DX_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "CodeDx (CSV)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(len(CODE_DX_PRESET_CSV)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        CODE_DX_PRESET_CSV[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        CODE_DX_PRESET_CSV[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "PMD (CSV)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(len(PMD_PRESET_CSV)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PMD_PRESET_CSV[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        PMD_PRESET_CSV[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "PHP_CodeSniffer(CSV)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(len(PHP_CODESNIFFER_PRESET_CSV)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PHP_CODESNIFFER_PRESET_CSV[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                       PHP_CODESNIFFER_PRESET_CSV[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "PHP_CodeSniffer(XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == PHP_CODESNIFFER_PRESET_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(PHP_CODESNIFFER_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PHP_CODESNIFFER_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        PHP_CODESNIFFER_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "PMD (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == PMD_PRESET_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(PMD_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PMD_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        PMD_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        # elif currText == "CodeDx (CSV w/Details)":
        #     self.tbl_Dataset.setRowCount(0)
        #     self.datasetColumns = []
        #     for i in range(len(CODE_DX_PRESET_CSV_DETAILS)):
        #         if i == 0:
        #             # First is output column
        #             dsCol = DatasetColumn(
        #                 CODE_DX_PRESET_CSV_DETAILS[i],
        #                 "Categorical",
        #                 "One-hot Encoding",
        #                 "Output",
        #                 "True Positive",
        #             )
        #         else:
        #             dsCol = DatasetColumn(
        #                 CODE_DX_PRESET_CSV_DETAILS[i],
        #                 "Categorical",
        #                 "One-hot Encoding",
        #                 "Input",
        #                 "",
        #             )
        #         self.datasetColumns.append(dsCol)
        #         new_row_idx = self.tbl_Dataset.rowCount()

        #         self.tbl_Dataset.insertRow(new_row_idx)

        #         self.tbl_Dataset.setItem(
        #             new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
        #         )
        #         self.tbl_Dataset.setItem(
        #             new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes")
        #         )
        #         self.tbl_Dataset.setItem(
        #             new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
        #         )
        #         self.tbl_Dataset.setItem(
        #             new_row_idx,
        #             3,
        #             QtWidgets.QTableWidgetItem(dsCol.Transformation),
        #         )
        #         self.tbl_Dataset.setItem(
        #             new_row_idx,
        #             4,
        #             QtWidgets.QTableWidgetItem(
        #                 dsCol.Type
        #                 if dsCol.TPLabel == ""
        #                 else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
        #             ),
        #         )
        elif currText == "Gendarme (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == GENDARME_PRESET_XML_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(GENDARME_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        GENDARME_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "True Positive",
                    )
                else:
                    dsCol = DatasetColumn(
                        GENDARME_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "SpotBugs (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == SPOTBUGS_PRESET_XML_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(SPOTBUGS_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        SPOTBUGS_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "True Positive",
                    )
                else:
                    dsCol = DatasetColumn(
                        SPOTBUGS_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "Fortify (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == FORTIFY_PRESET_XML_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(FORTIFY_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        FORTIFY_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "True Positive",
                    )
                else:
                    dsCol = DatasetColumn(
                        FORTIFY_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "Pylint (JSON)":
            self.cBox_Preset_selected_json(currText)
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.ds_xml_dict = {}
            for i in range(len(PYLINT_PRESET_JSON)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PYLINT_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        PYLINT_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "PHP_CodeSniffer(JSON)":
            self.cBox_Preset_selected_json(currText)
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.ds_xml_dict = {}
            for i in range(len(PHP_CODESNIFFER_PRESET_JSON)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PHP_CODESNIFFER_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        PHP_CODESNIFFER_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "PMD (JSON)":
            self.cBox_Preset_selected_json(currText)
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.ds_xml_dict = {}
            for i in range(len(PMD_PRESET_JSON)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        PMD_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        PMD_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "ESLint (JSON)":
            self.cBox_Preset_selected_json(currText)
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.ds_xml_dict = {}
            for i in range(len(ESLINT_PRESET_JSON)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        ESLINT_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        ESLINT_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "CppCheck (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == CPPCHECK_PRESET_XML_ROOT:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(CPPCHECK_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        CPPCHECK_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "True Positive",
                    )
                else:
                    dsCol = DatasetColumn(
                        CPPCHECK_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "JSHint (XML)":
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            for i in range(self.cBox_Root.count()):
                if self.cBox_Root.itemText(i) == JSHINT_PRESET_XML:
                    self.cBox_Root.setCurrentIndex(i)
                    break
            for i in range(len(JSHINT_PRESET_XML)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        JSHINT_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        JSHINT_PRESET_XML[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )
        elif currText == "JSHint (JSON)":
            self.cBox_Preset_selected_json(currText)
            self.tbl_Dataset.setRowCount(0)
            self.datasetColumns = []
            self.ds_xml_dict = {}
            for i in range(len(JSHINT_PRESET_JSON)):
                if i == 0:
                    # First is output column
                    dsCol = DatasetColumn(
                        JSHINT_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Output",
                        "escalated",
                    )
                else:
                    dsCol = DatasetColumn(
                        JSHINT_PRESET_JSON[i],
                        "Categorical",
                        True,
                        "One-hot Encoding",
                        "Input",
                        "",
                    )
                self.datasetColumns.append(dsCol)
                new_row_idx = self.tbl_Dataset.rowCount()

                self.tbl_Dataset.insertRow(new_row_idx)

                self.tbl_Dataset.setItem(
                    new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
                )
                self.tbl_Dataset.setItem(
                    new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    3,
                    QtWidgets.QTableWidgetItem(dsCol.Transformation),
                )
                self.tbl_Dataset.setItem(
                    new_row_idx,
                    4,
                    QtWidgets.QTableWidgetItem(
                        dsCol.Type
                        if dsCol.TPLabel == ""
                        else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
                    ),
                )

    def btn_AddColumn_clicked(self):
        """clicked event on btn_AddColumn
        Adds a column if it doesnt exist to our table and to our column list.
        """
        name = self.cBox_Column.currentText()
        data = self.cBox_Data.currentText()
        training = True if self.cBox_Training.currentText() == "Yes" else False
        transformation = self.cBox_Transformation.currentText()
        col_type = self.cBox_Type.currentText()
        if col_type == "Output":
            tp_label = self.cBox_TPLabel.currentText()
        else:
            tp_label = ""
        dsCol = DatasetColumn(name, data, training, transformation, col_type, tp_label)

        numRows = self.tbl_Dataset.rowCount()
        new_row_idx = numRows
        for i in range(numRows):
            if (
                self.tbl_Dataset.item(i, 0) is not None
                and dsCol.Name == self.tbl_Dataset.item(i, 0).text()
            ):
                new_row_idx = i
                self.tbl_Dataset.removeRow(new_row_idx)

        self.tbl_Dataset.insertRow(new_row_idx)

        self.tbl_Dataset.setItem(
            new_row_idx, 0, QtWidgets.QTableWidgetItem(dsCol.Name)
        )
        self.tbl_Dataset.setItem(
            new_row_idx, 1, QtWidgets.QTableWidgetItem("Yes" if dsCol.Training else "No")
        )
        self.tbl_Dataset.setItem(
            new_row_idx, 2, QtWidgets.QTableWidgetItem(dsCol.Data)
        )
        self.tbl_Dataset.setItem(
            new_row_idx, 3, QtWidgets.QTableWidgetItem(dsCol.Transformation)
        )
        self.tbl_Dataset.setItem(
            new_row_idx,
            4,
            QtWidgets.QTableWidgetItem(
                dsCol.Type
                if dsCol.TPLabel == ""
                else "{} ({})".format(dsCol.Type, dsCol.TPLabel)
            ),
        )

        existingColumn = False
        for i in range(len(self.datasetColumns)):
            if self.datasetColumns[i].Name == dsCol.Name:
                self.datasetColumns[i] = dsCol
                existingColumn = True
                break
        if not existingColumn:
            self.datasetColumns.append(dsCol)

    def btn_RemoveColumn_clicked(self):
        """clicked event on btn_RemoveColumn
        Removes a column from column table and column list.
        Uses for current selected row to perform deletion.
        """
        numRows = self.tbl_Dataset.rowCount()
        assert numRows == len(self.datasetColumns)

        indexes = list(
            sorted(
                set(
                    index.row() for index in self.tbl_Dataset.selectedIndexes()
                )
            )
        )
        if len(indexes) > 0:
            del_row_idx = indexes[0]
            self.tbl_Dataset.removeRow(del_row_idx)
            del self.datasetColumns[del_row_idx]

    def hSld_TrainTestSplit_valueChanged(self):
        """valueChanged event on hSld_TrainTestSplit
        Displays train/test percentage.
        """
        trainSplit = self.hSld_TrainTestSplit.value()
        self.txtB_TrainPercentage.setText("{0}".format(trainSplit))
        self.txtB_TestPercentage.setText("{0}".format(100 - trainSplit))

    def btn_SaveSchema_clicked(self):
        """clicked event on btn_Schema
        Saves current schema to a json file at specified location.
        """
        numColumns = len(self.datasetColumns)
        print(self.datasetColumns)
        print(len(self.datasetColumns))
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
        numInputColumns = len(
            [c for c in self.datasetColumns if c.Type == "Input"]
        )
        if numInputColumns == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Wrong input column!")
            msg.setText(
                "Please, make sure that you have at least one input column."
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
                jsonDict = DatasetColumn.CreateJson(
                    self.datasetColumns,
                    self.txtB_DatasetPath.text(),
                    self.hSld_TrainTestSplit.value(),
                    self.df_dataset,
                )
            elif self.dataset_type == "xml":
                jsonDict = DatasetColumn.CreateJson(
                    self.datasetColumns,
                    self.txtB_DatasetPath.text(),
                    self.hSld_TrainTestSplit.value(),
                    self.df_dataset,
                    {"root": self.ds_roots[self.cBox_Root.currentIndex()]},
                )
            elif self.dataset_type == "json":
                jsonDict = DatasetColumn.CreateJson(
                    self.datasetColumns,
                    self.txtB_DatasetPath.text(),
                    self.hSld_TrainTestSplit.value(),
                    self.df_dataset,
                )                
            with open(fileName, "w", encoding="utf-8") as fp:
                json.dump(jsonDict, fp)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("File saved successfully!")
            msg.setWindowTitle("File saved")
            msg.exec_()

