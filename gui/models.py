import json
import numpy as np
import pandas as pd
import tensorflow as tf
from help import Impl_HelpWindow
from datasets_workers import WorkerLoadXMLCols, WorkerLoadXMLDataset
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from models_ui import Ui_ModelsWindow
from models_workers import WorkerTrainModel


class Impl_ModelsWindow(Ui_ModelsWindow, QtWidgets.QMainWindow):
    """Creates models window"""

    def __init__(self):
        """Initializes models window object"""
        super(Impl_ModelsWindow, self).__init__()
        self.setupUi(self)

        self.customEvents()
        self.customInit()

    def customEvents(
        self,
    ):
        """Custom events method; here you connect functions with the UI."""
        self.btn_LoadSchema.clicked.connect(self.btn_LoadSchema_clicked)
        self.btn_TrainNow.clicked.connect(self.btn_TrainNow_clicked)
        self.btn_SaveModel.clicked.connect(self.btn_SaveModel_clicked)
        self.btn_Help.clicked.connect(self.btn_Help_clicked)
        self.cBox_EvaluateDataset.currentTextChanged.connect(
            self.cBox_EvaluateDataset_currentTextChanged
        )
        self.dsBox_Threshold.valueChanged.connect(
            self.dsBox_Threshold_valueChanged
        )
        self.btn_Help.clicked.connect(self.btn_Help_clicked)

    def btn_Help_clicked(self):
        """Clicked event on btn_Help component.
        Loads and show Help Window.
        """
        self.hs_ui = Impl_HelpWindow("Models")
        self.hs_ui.show()

    def customInit(self):
        """Custom init method"""
        self.pBar_TrainProgress.setValue(0)
        self.model = None
        self.btn_TrainNow.setEnabled(False)

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

    def evtWorkerLoadXMLSchemaCols(self, params):
        """Thread method to load columns of xml dataset.

        Args:
            params (dict): Dictionary containing ds_cols
        """
        self.ds_cols = params["ds_cols"]
        self.df_dataset = self.createDataFrameFromXML(self.d, self.ds_cols)
        self.statusBar().showMessage("Loading XML Dataset done!", 3000)
        self.btn_TrainNow.setEnabled(True)

    def evtWorkerLoadXMLSchema(self, params):
        """Thread method to load XML schema file.

        Args:
            params (dict): Dictionary containing ds_xml_dict and ds_roots.
        """
        self.ds_xml_dict = params["ds_xml_dict"]
        self.ds_roots = params["ds_roots"]

        if not (self.ds_xml_dict or self.ds_roots):
            self.clearDatasetInfo()
            self.btn_TrainNow.setEnabled(False)
            return

        selectedRoot = self.schemaDict["xml_params"]["root"]
        self.d = self.ds_xml_dict.copy()
        for c in selectedRoot:
            self.d = self.d[c]

        self.worker_xml_schema_cols = WorkerLoadXMLCols(self.d, parent=self)
        self.worker_xml_schema_cols.start()
        self.worker_xml_schema_cols.worker_complete.connect(
            self.evtWorkerLoadXMLSchemaCols
        )

    def loadDataset(self):
        """Loads a dataset either in CSV or XML format."""
        if self.schemaDict["format"] == "csv":
            try:
                self.df_dataset = pd.read_csv(self.schemaDict["filename"])
            except FileNotFoundError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "The file at '{}' could not be loaded or it doesn't exists. \nPlease fix the filename and then try again.".format(
                        self.schemaDict["filename"]
                    )
                )
                msg.setWindowTitle("Wrong file on schema file.")
                msg.exec_()
                self.clearDatasetInfo()
                self.btn_TrainNow.setEnabled(False)
                return
            self.btn_TrainNow.setEnabled(True)
        elif self.schemaDict["format"] == "xml":

            self.statusBar().showMessage("Loading XML Dataset, please wait...")
            self.worker_xml_schema = WorkerLoadXMLDataset(
                self.schemaDict["filename"], parent=self
            )
            self.worker_xml_schema.start()
            self.worker_xml_schema.worker_complete.connect(
                self.evtWorkerLoadXMLSchema
            )

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

            df = self.df_dataset
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
                c for c in self.schemaDict["columns"] if c["type"] == "Output"
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

        # self.lbl_TrainProgress.setText(
        #    "Epoch {}/{} ({:.2f}%)".format(0, self.epochs, 0))

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
            self.loadDataset()

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

    def clearDatasetInfo(self):
        """Clears dataset information on display text boxes."""
        self.txtB_DatasetPath.setText("")
        self.txtB_InfoFeatures.setText("")
        self.txtB_InfoTrainSamples.setText("")
        self.txtB_InfoTestSamples.setText("")
