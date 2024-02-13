from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import xmltodict
import zipfile
import os
from vinci_utils import findRoots, findColumns


class WorkerLoadXMLCols(QThread):
    """Worker thread class to load columns from an XML given a root.

    Args:
        QThread (QThread): Used for inheritance.
    """

    def __init__(self, d, parent=None):
        """Construct a worker to load XML columns.

        Args:
            d (dict): XML as a dict
            parent (optional): Defaults to None.
        """
        QThread.__init__(self, parent)
        self.d = d

    worker_complete = pyqtSignal(dict)

    def run(self):
        """Loads xml columns"""
        allColumns = []
        for i in range(len(self.d)):
            columns = findColumns(self.d[i], [], [])
            for c in columns:
                if c not in allColumns:
                    allColumns.append(c)
        ds_cols = sorted(allColumns)

        self.worker_complete.emit({"ds_cols": ds_cols})


class WorkerLoadXMLDataset(QThread):
    """Worker thread class to load an XML Dataset.

    Args:
        QThread (QThread): Used for inheritance.
    """

    def __init__(self, filepath, parent=None):
        """Construct a worker to load a dataset.

        Args:
            filepath (str): File path to the dataset.
            parent (optional): Defaults to None.
        """
        QThread.__init__(self, parent)
        self.filepath = filepath

    worker_complete = pyqtSignal(dict)

    def run(self):
        """Loads a dataset either in xml format."""
        dataset_type = os.path.splitext(self.filepath)[1][1:].lower()
        ds_xml_dict = {}
        ds_roots = []
        try:
            if dataset_type == "xml":
                with open(self.filepath, "r", encoding="utf-8") as fp:
                    content = fp.read()
                ds_xml_dict = xmltodict.parse(content)

                ds_roots = findRoots(ds_xml_dict, [], [])
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(
                "The file at '{}' could not be loaded or it doesn't exists. \nPlease fix the filename and then try again.".format(
                    self.filepath
                )
            )
            msg.setWindowTitle("Wrong file on schema file.")
            msg.exec_()
            ds_xml_dict = {}
            ds_roots = []
            ds_raw = ""

        self.worker_complete.emit(
            {
                "ds_xml_dict": ds_xml_dict,
                "ds_roots": ds_roots,
                "ds_raw": str(content),
            }
        )


class WorkerLoadFPRDataset(QThread):
    """Worker thread class to load an XML Dataset from a Fortify FPR file.

    Args:
        QThread (QThread): Used for inheritance.
    """

    def __init__(self, filepath, parent=None):
        """Construct a worker to load a dataset.

        Args:
            filepath (str): File path to the dataset.
            parent (optional): Defaults to None.
        """
        QThread.__init__(self, parent)
        self.filepath = filepath

    worker_complete = pyqtSignal(dict)

    def run(self):
        """Loads a dataset either in xml format."""
        dataset_type = os.path.splitext(self.filepath)[1][1:].lower()
        ds_xml_dict = {}
        ds_roots = []
        if dataset_type == "fpr":
            with zipfile.ZipFile(self.filepath, "r") as zip:
                content = zip.read("audit.fvdl")
            ds_xml_dict = xmltodict.parse(content)

            ds_roots = findRoots(ds_xml_dict, [], [])

        self.worker_complete.emit(
            {
                "ds_xml_dict": ds_xml_dict,
                "ds_roots": ds_roots,
                "ds_raw": content,
            }
        )


class WorkerLoadZIPDataset(QThread):
    """Worker thread class to load an XML Dataset from a CppCheck ZIP file.

    Args:
        QThread (QThread): Used for inheritance.
    """

    def __init__(self, filepath, parent=None):
        """Construct a worker to load a dataset.

        Args:
            filepath (str): File path to the dataset.
            parent (optional): Defaults to None.
        """
        QThread.__init__(self, parent)
        self.filepath = filepath

    worker_complete = pyqtSignal(dict)

    def run(self):
        """Loads a dataset either in xml format."""
        dataset_type = os.path.splitext(self.filepath)[1][1:].lower()
        ds_xml_dict = {}
        ds_roots = []
        if dataset_type == "zip":
            with zipfile.ZipFile(self.filepath, "r") as zip:
                valid_files = [file for file in zip.namelist() if file.endswith(".xml")]
                valid_file = valid_files[0]
                content = zip.read(valid_file)
            ds_xml_dict = xmltodict.parse(content)

            ds_roots = findRoots(ds_xml_dict, [], [])

        self.worker_complete.emit(
            {
                "ds_xml_dict": ds_xml_dict,
                "ds_roots": ds_roots,
                "ds_raw": content,
            }
        )
