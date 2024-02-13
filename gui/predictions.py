import pandas as pd
import numpy as np
import tensorflow as tf
import json
from predictions_ui import Ui_PredictionsWindow
from datasets_workers import WorkerLoadXMLDataset, WorkerLoadXMLCols
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from help import Impl_HelpWindow


class Impl_PredictionsWindow(Ui_PredictionsWindow, QtWidgets.QMainWindow):
    """Creates predictions window"""

    def __init__(self):
        """Initializes predictions window object"""
        super(Impl_PredictionsWindow, self).__init__()
        self.setupUi(self)

        self.customEvents()
        self.customInit()

    def customEvents(self):
        """Custom events method; here you connect functions with the UI."""
        self.btn_LoadDataset.clicked.connect(self.btn_LoadDataset_clicked)
        self.btn_LoadSchema.clicked.connect(self.btn_LoadSchema_clicked)
        self.btn_LoadModel.clicked.connect(self.btn_LoadModel_clicked)
        self.btn_Predict.clicked.connect(self.btn_Predict_clicked)
        self.btn_SaveResults.clicked.connect(self.btn_SaveResults_clicked)
        self.btn_Help.clicked.connect(self.btn_Help_clicked)

    def customInit(self):
        """Custom init method"""
        self.btn_Predict.setEnabled(False)
        self.btn_SaveResults.setEnabled(False)
        self.df_dataset = None
        self.schemaDict = None
        self.model = None
        self.tp_label = None
        self.preds = None
        self.bin_preds = None

    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
        Loads and show Help Window.
        """
        self.hs_ui = Impl_HelpWindow("Prediction")
        self.hs_ui.show()

    def createDataFrameFromXML(self, dict_list, ds_cols):
        """Creates a pandas DataFrame from an XML file.

        Args:
            dict_list (list(dict)): List of dictionaries, each entry represents a row.
            ds_cols (list(list(str))): List of data columns that should be extracted.

        Returns:
            df_dataset (pd.DataFrame): Pandas DataFrame representation of XML dataset.
        """
        col_data = [[] for _ in range(len(ds_cols))]

        for entry in dict_list:
            for i in range(len(ds_cols)):
                curr_col = ds_cols[i]
                value = entry
                for j in range(len(curr_col)):
                    if value is None or curr_col[j] not in value:
                        value = ""
                        break
                    value = value[curr_col[j]]
                col_data[i].append(value)
        cols = ["->".join(c) for c in ds_cols]

        df_dataset = pd.DataFrame()

        for i in range(len(cols)):
            df_dataset[cols[i]] = col_data[i]

        return df_dataset

    def evtWorkerLoadXMLSchemaCols(self, params):
        """Thread method that loads xml schema columns

        Args:
            params (dict): Dictionary containing ds_cols
        """
        self.ds_cols = params["ds_cols"]
        self.df_dataset = self.createDataFrameFromXML(self.d, self.ds_cols)
        self.statusBar().showMessage("Loading XML Dataset done!", 3000)
        self.btn_Predict.setEnabled(True)
        self.txtB_InfoSamples.setText("{}".format(self.df_dataset.shape[0]))

    def evtWorkerLoadXMLSchema(self, params):
        """Thread method that loads an XML schema

        Args:
            params (dict): Dictionary containing ds_xml_dict and ds_roots
        """
        self.ds_xml_dict = params["ds_xml_dict"]
        self.ds_roots = params["ds_roots"]
        selectedRoot = self.schemaDict["xml_params"]["root"]
        self.d = self.ds_xml_dict.copy()
        for c in selectedRoot:
            self.d = self.d[c]

        self.worker_xml_schema_cols = WorkerLoadXMLCols(self.d)
        self.worker_xml_schema_cols.start()
        self.worker_xml_schema_cols.worker_complete.connect(
            self.evtWorkerLoadXMLSchemaCols
        )

    def loadDataframe(self, filename):
        """Loads a dataframe from filepath

        Args:
            filename (str): File path to dataframe.
        """
        if self.schemaDict["format"] == "csv":
            self.df_dataset = pd.read_csv(filename)
            self.btn_Predict.setEnabled(True)
            self.txtB_InfoSamples.setText("{}".format(self.df_dataset.shape[0]))
        elif self.schemaDict["format"] == "xml":
            self.statusBar().showMessage("Loading XML Dataset, please wait...")
            self.worker_xml_schema = WorkerLoadXMLDataset(filename)
            self.worker_xml_schema.start()
            self.worker_xml_schema.worker_complete.connect(self.evtWorkerLoadXMLSchema)

    def btn_LoadDataset_clicked(self):
        """clicked event on btn_LoadDataset
        Opens a file dialog to load a dataset.
        """
        widget = QtWidgets.QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            widget,
            "Open Dataset File",
            "",
            "CSV|XML Files (*.csv *.xml)",
            options=options,
        )
        if fileName:
            self.txtB_DatasetPath.setText(fileName)
        if self.checkFilesHealth():
            self.loadDataframe(self.txtB_DatasetPath.text())

    def btn_LoadSchema_clicked(self):
        """clicked event on btn_LoadSchema
        Opens a file dialog to load a JSON schema file.
        """
        widget = QtWidgets.QWidget()
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
            with open(fileName, "r", encoding="utf-8") as fp:
                self.schemaDict = json.load(fp)
                self.txtB_SchemaPath.setText(fileName)
        if self.checkFilesHealth():
            self.loadDataframe(self.txtB_DatasetPath.text())

    def btn_LoadModel_clicked(self):
        """clicked event on btn_LoadModel
        Loads a .h5 trained model.
        """
        widget = QtWidgets.QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            widget, "Open Model File", "", "H5 Files (*.h5)", options=options
        )
        if fileName:
            self.model = tf.keras.models.load_model(fileName)
            self.txtB_ModelPath.setText(fileName)
        if self.checkFilesHealth():
            self.loadDataframe(self.txtB_DatasetPath.text())

    def checkFilesHealth(self):
        """Checks that dataset, schema and model files are healthy.

        Returns:
            bool: Whether all files are valid or not.
        """
        dataset_check = self.txtB_DatasetPath.text() != ""
        schema_check = self.txtB_SchemaPath.text() != "" and self.schemaDict is not None
        model_check = self.txtB_ModelPath.text() != "" and self.model is not None
        return dataset_check and schema_check and model_check

    def extractData(self):
        """Extracts data from dataset into numpy arrays.

        Returns:
            tuple(X:np.ndarray, tp_label:str): Input values for model and true positive label.
        """
        outputColumn = [c for c in self.schemaDict["columns"] if c["type"] == "Output"][
            0
        ]

        num_df = pd.DataFrame()
        for col in self.schemaDict["columns"]:
            if col["type"] == "Input" and col["training"]:
                num_unique = col["num_unique"]
                unique = col["unique"]
                col_values = self.df_dataset[col["name"]].values.tolist()
                curr_feature = [[0 for _ in range(num_unique)] for _ in range(len(col_values))]
                for i, val in enumerate(col_values):
                    try:
                        col_idx = unique.index(val)
                        curr_feature[i][col_idx] = 1
                    except ValueError:
                        col_idx = -1
                dummy_col_names = ["{}_{}".format(col["name"], i) for i in range(num_unique)]
                curr_feature = pd.DataFrame(
                    curr_feature, columns=dummy_col_names
                )
                num_df = pd.concat([num_df, curr_feature], axis=1)

        # output_df = (self.df_dataset[outputColumn["name"]] ==
        #             outputColumn["tplabel"]).astype(int)
        # output_df = pd.DataFrame({outputColumn["name"]: output_df})

        # num_df = pd.concat([num_df, output_df], axis=1)

        X = num_df.values
        tp_label = outputColumn["tplabel"]

        return X, tp_label

    def btn_Predict_clicked(self):
        """clicked event on btn_Predict
        Performs inference and stores predictions in memory.
        """
        X, tp_label = self.extractData()

        self.tp_label = tp_label
        self.preds = self.model.predict(X)
        self.bin_preds = np.floor(
            self.preds + (1 - self.dsBox_Threshold.value())
        ).astype(int)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Predictions have been done! Now you can save the results.")
        msg.setWindowTitle("Predictions done")
        msg.exec_()
        self.btn_SaveResults.setEnabled(True)

    def btn_SaveResults_clicked(self):
        """Saves previously produced inference results to a CSV file."""
        if (
            self.tp_label is not None
            and self.preds is not None
            and self.bin_preds is not None
        ):

            widget = QWidget()
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(
                widget,
                "Save Results File",
                "",
                "CSV Files (*.csv)",
                options=options,
            )
            if fileName:
                fileName = (
                    fileName + ".csv" if not fileName.endswith(".csv") else fileName
                )
                preds_df = pd.DataFrame()
                bin_preds_label = self.bin_preds.copy()
                bin_preds_label = bin_preds_label.astype(object)
                bin_preds_label[self.bin_preds.astype(bool)] = self.tp_label
                bin_preds_label[~self.bin_preds.astype(bool)] = "False"
                bin_preds_label = np.squeeze(bin_preds_label)

                preds_df["{}_predicted".format(self.tp_label)] = bin_preds_label
                preds_df["{}_values_predicted".format(self.tp_label)] = self.preds
                preds_df["{}_binary_predicted".format(self.tp_label)] = self.bin_preds

                results_df = pd.concat([self.df_dataset, preds_df], axis=1)
                results_df.to_csv(fileName)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Results saved successfully at {}".format(fileName))
                msg.setWindowTitle("Results saved!")
                msg.exec_()
