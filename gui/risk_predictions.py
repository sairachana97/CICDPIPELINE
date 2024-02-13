from risk_predictions_ui import Ui_RiskPredictionsWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
import pandas as pd
import json
import tensorflow as tf
import numpy as np

class Impl_RiskPredictionsWindow(Ui_RiskPredictionsWindow, QtWidgets.QMainWindow):
    """Creates risk predictions window"""

    def __init__(self):
        """Initializes risk predictions window object"""
        super(Impl_RiskPredictionsWindow, self).__init__()
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
            "CSV Files (*.csv)",
            options=options,
        )
        if fileName:
            self.txtB_DatasetPath.setText(fileName)
        if self.checkFilesHealth():
            self.loadDataframe(self.txtB_DatasetPath.text())

    def loadDataframe(self, filename):
        """Loads a dataframe from filepath

        Args:
            filename (str): File path to dataframe.
        """
        self.df_dataset = pd.read_csv(filename)
        self.btn_Predict.setEnabled(True)
        self.txtB_InfoSamples.setText("{}".format(self.df_dataset.shape[0]))
        
    def checkFilesHealth(self):
        """Checks that dataset file is healthy.

        Returns:
            bool: Whether the file is valid or not.
        """
        dataset_check = self.txtB_DatasetPath.text() != ""
        return dataset_check
    
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
                bin_preds_label[~self.bin_preds.astype(bool)] = "low"
                bin_preds_label = np.squeeze(bin_preds_label)

                preds_df["{}_predicted".format(self.tp_label)] = bin_preds_label

                results_df = pd.concat([self.df_dataset, preds_df], axis=1)
                results_df.to_csv(fileName)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Results saved successfully at {}".format(fileName))
                msg.setWindowTitle("Results saved!")
                msg.exec_()
