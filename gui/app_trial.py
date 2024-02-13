import sys
from PyQt5 import QtWidgets
from menu import Impl_MainWindow
from vinci_lic import checkLicense
from datasets_labeler import Impl_DatasetsLabelerWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if checkLicense():
        ui = Impl_MainWindow()
        ui.show()
        sys.exit(app.exec_())
