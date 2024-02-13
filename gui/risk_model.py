import json
import numpy as np
import pandas as pd
import tensorflow as tf
from help import Impl_HelpWindow
from risk_model_ui import Ui_RiskModelWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from models_workers import WorkerTrainModel


class Impl_RiskModelWindow(Ui_RiskModelWindow, QtWidgets.QMainWindow):
    """Creates models window"""

    def __init__(self, datasetDF):
        """Initializes models window object"""
        super(Impl_RiskModelWindow, self).__init__()
        self.dataserDF = datasetDF
        self.setupUi(self)
        self.customEvents()

    def customEvents(
            self,
    ):
        """Custom events method; here you connect functions with the UI."""
        self.btn_Help.clicked.connect(self.btn_Help_clicked)
        self.btn_LoadSchema.clicked.connect(self.btn_LoadSchema_clicked)
        self.btn_SaveModel.clicked.connect(self.btn_SaveModel_clicked)
        self.btn_TrainNow.clicked.connect(self.btn_TrainNow_clicked)
        self.cBox_EvaluateDataset.currentTextChanged.connect(
            self.cBox_EvaluateDataset_currentTextChanged
        )
        self.dsBox_Threshold.valueChanged.connect(
            self.dsBox_Threshold_valueChanged
        )

    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
        Loads and show Help Window.
        """
        self.hs_ui = Impl_HelpWindow("Risk Model")
        self.hs_ui.show()

    def btn_LoadSchema_clicked(self):
        """clicked event on btn_LoadSchema
        Loads an schema file.
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
            self.txtB_DatasetPath.setText(fileName)
            self.fillDatasetInfo()

    def fillDatasetInfo(self):
        """Fills dataset information into display text boxes."""
        self.txtB_InfoFeatures.setText(
            "{}".format(len(self.schemaDict["columns"]))
        )
        self.txtB_InfoTrainSamples.setText(
            "{}".format(len(self.schemaDict["trainIdx"]))
        )
        self.txtB_InfoTestSamples.setText(
            "{}".format(len(self.schemaDict["testIdx"]))
        )
    
    def extractDataset(self, split: str):
        """Extracts a dataset from a schema file specification
        given a split, ie. train/test.

        Args:
            split (str): Split to use. Either 'train' or 'test'

        Returns:
            tuple(X:np.ndarray,Y:np.ndarray): Input X and output Y of selected split.
        """
        if self.schemaDict["format"] == "csv":
            outputColumn = [
                c for c in self.schemaDict["columns"] if c["type"] == "Output"
            ][0]
            df = self.dataserDF
            if split == "train":
                idx = self.schemaDict["trainIdx"]
            elif split == "test":
                idx = self.schemaDict["testIdx"]

            num_df = pd.DataFrame()
            for col in self.schemaDict["columns"]:
                if col["type"] == "Input" and col["training"]:
                    num_unique = col["num_unique"]
                    unique = col["unique"]
                    col_values = df[col["name"]].values.tolist()
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

            output_df = (
                df[outputColumn["name"]] == outputColumn["tplabel"]
            ).astype(int)
            output_df = pd.DataFrame({outputColumn["name"]: output_df})

            num_df = pd.concat([num_df, output_df], axis=1)

            num_df = num_df[df.index.isin(idx)]

            X = num_df.drop(columns=[outputColumn["name"]]).values
            Y = num_df[outputColumn["name"]].values

            return X, Y
        elif self.schemaDict["format"] == "xml":
            outputColumn = [
                c for c in self.schemaDict["columns"] if c["type"] == "risk_level"
            ][0]

            df = self.df_dataset
            if split == "train":
                idx = self.schemaDict["trainIdx"]
            elif split == "test":
                idx = self.schemaDict["testIdx"]

            num_df = pd.DataFrame()
            for col in self.schemaDict["columns"]:
                if col["type"] == "Input" and col["training"]:
                    curr_feature = pd.get_dummies(
                        df[col["name"]], prefix=col["name"]
                    )
                    num_df = pd.concat([num_df, curr_feature], axis=1)

            output_df = (
                df[outputColumn["name"]] == outputColumn["tplabel"]
            ).astype(int)
            output_df = pd.DataFrame({outputColumn["name"]: output_df})

            num_df = pd.concat([num_df, output_df], axis=1)

            num_df = num_df[df.index.isin(idx)]

            X = num_df.drop(columns=[outputColumn["name"]]).values
            Y = num_df[outputColumn["name"]].values

            return X, Y
        
    def btn_TrainNow_clicked(self):
        """clicked event on btn_TrainNow
        Starts model training.
        """
        self.lr = float(self.txtB_LearningRate.text())
        self.epochs = int(self.sBox_Epochs.value())
        X, Y = self.extractDataset("train")
        input_shape = X.shape[1]
        custom_metrics = []
        if self.cBox_MetricsAccuracy.isChecked():
            custom_metrics.append("accuracy")
        if self.cBox_MetricsPrecision.isChecked():
            custom_metrics.append("precision")
        if self.cBox_MetricsRecall.isChecked():
            custom_metrics.append("recall")

        self.btn_TrainNow.setEnabled(False)
        self.lbl_TrainProgress.setText(
            "We are training your model, please wait..."
        )
        self.statusBar().showMessage("Training model, please wait...")

        self.worker_train_model = WorkerTrainModel(
            X,
            Y,
            input_shape,
            self.epochs,
            self.lr,
            custom_metrics,
            parent=self,
        )
        self.worker_train_model.start()
        self.worker_train_model.worker_complete.connect(
            self.evtWorkerTrainModelFinished
        )

    def btn_SaveModel_clicked(self):
        """clicked event on btn_SaveModel
        Saves model to a .h5 file."""
        widget = QWidget()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            widget, "Save Model File", "", "H5 Files (*.h5)", options=options
        )
        if fileName:
            fileName = (
                fileName + ".h5" if not fileName.endswith(".h5") else fileName
            )
            self.model.save(fileName)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Model saved successfully at {}".format(fileName))
            msg.setWindowTitle("Model saved!")
            msg.exec_()

    def evtWorkerTrainModelFinished(self, params):
        """Thread method to update UI when model training has finished.

        Args:
            params (dict): Dictionary containing trained model.
        """
        self.model = params["model"]

        self.btn_TrainNow.setEnabled(True)
        self.lbl_TrainProgress.setText("Model training finished!")
        self.statusBar().showMessage("Training model done!", 5000)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Model training successful!")
        msg.setWindowTitle("Model training")
        msg.exec_()
        self.pBar_TrainProgress.setValue(100)
        self.btn_SaveModel.setEnabled(True)

        self.cBox_EvaluateDataset.clear()
        self.cBox_EvaluateDataset.addItems(["Train", "Test"])

    def cBox_EvaluateDataset_currentTextChanged(self):
        """currentTextChanged event on cBox_EvaluateDataset
        Calculates new predictions and metrics when selected dataset changes.
        """
        if (
            self.model is not None
            and self.cBox_EvaluateDataset.currentText()
            in [
                "Train",
                "Test",
            ]
        ):
            subset = self.cBox_EvaluateDataset.currentText().lower()
            X, Y = self.extractDataset(subset)

            if X.shape[0] > 0 and Y.shape[0] > 0:  #If set is not empty
                preds = self.model.predict(X)

                bce = tf.keras.losses.BinaryCrossentropy(from_logits=True)
                loss = bce(Y, np.squeeze(preds,axis=1)).numpy()

                bin_preds = np.floor(
                    preds + (1 - self.dsBox_Threshold.value())
                ).astype(int)

                (
                    TP,
                    TN,
                    FP,
                    FN,
                    accuracy,
                    precision,
                    recall,
                    f1_score,
                ) = self.calculateMetrics(Y, bin_preds.T)
            else:
                loss = 0
                (
                    TP,
                    TN,
                    FP,
                    FN,
                    accuracy,
                    precision,
                    recall,
                    f1_score,
                ) = (0,0,0,0,0,0,0,0)

            self.txtB_EvalMetricsLoss.setText("{:.4f}".format(loss))
            self.txtB_EvalMetricsTP.setText("{}".format(TP))
            self.txtB_EvalMetricsTN.setText("{}".format(TN))
            self.txtB_EvalMetricsFP.setText("{}".format(FP))
            self.txtB_EvalMetricsFN.setText("{}".format(FN))
            self.txtB_EvalMetricsAccuracy.setText("{:.4f}".format(accuracy))
            self.txtB_EvalMetricsPrecision.setText("{:.4f}".format(precision))
            self.txtB_EvalMetricsRecall.setText("{:.4f}".format(recall))
            self.txtB_EvalMetricsF1.setText("{:.4f}".format(f1_score))

    def dsBox_Threshold_valueChanged(self):
        """valueChanged event on dsBox_Threshold
        Calculates new predictions and metrics when selected evaluation threshold changes.
        """
        if (
            self.model is not None
            and self.cBox_EvaluateDataset.currentText()
            in [
                "Train",
                "Test",
            ]
        ):
            subset = self.cBox_EvaluateDataset.currentText().lower()
            X, Y = self.extractDataset(subset)

            preds = self.model.predict(X)

            bce = tf.keras.losses.BinaryCrossentropy(from_logits=True)
            loss = bce(Y, np.squeeze(preds)).numpy()

            self.txtB_EvalMetricsLoss.setText("{:.4f}".format(loss))

            bin_preds = np.floor(
                preds + (1 - self.dsBox_Threshold.value())
            ).astype(int)

            (
                TP,
                TN,
                FP,
                FN,
                accuracy,
                precision,
                recall,
                f1_score,
            ) = self.calculateMetrics(Y, bin_preds.T)

            self.txtB_EvalMetricsTP.setText("{}".format(TP))
            self.txtB_EvalMetricsTN.setText("{}".format(TN))
            self.txtB_EvalMetricsFP.setText("{}".format(FP))
            self.txtB_EvalMetricsFN.setText("{}".format(FN))
            self.txtB_EvalMetricsAccuracy.setText("{:.4f}".format(accuracy))
            self.txtB_EvalMetricsPrecision.setText("{:.4f}".format(precision))
            self.txtB_EvalMetricsRecall.setText("{:.4f}".format(recall))
            self.txtB_EvalMetricsF1.setText("{:.4f}".format(f1_score))

    def calculateMetrics(self, Y_true, Y_pred):
        """Calculates performance metrics.
        Metrics include accuracy, precision, recall and f1 score.

        Args:
            Y_true (np.ndarray): True output values
            Y_pred (np.ndarray): Predicted output values

        Returns:
            tuple: Results of TP, TN, FP, FN and metrics.
        """
        TP = ((Y_pred == 1) & (Y_true == 1)).sum()
        TN = ((Y_pred == 0) & (Y_true == 0)).sum()
        FP = ((Y_pred == 1) & (Y_true == 0)).sum()
        FN = ((Y_pred == 0) & (Y_true == 1)).sum()
        eps = 1e-6
        accuracy = (TP + TN) / (TP + FP + FN + TN + eps)
        precision = TP / (TP + FP + eps)
        recall = TP / (TP + FN + eps)
        f1_score = 2 * (recall * precision) / (recall + precision + eps)

        return TP, TN, FP, FN, accuracy, precision, recall, f1_score
