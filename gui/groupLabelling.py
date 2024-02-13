import pandas as pd
from groupLabelling_ui import Ui_Dialog
from PyQt5 import QtWidgets

class Impl_GroupLabelling_Window(Ui_Dialog, QtWidgets.QMainWindow):
    """Creates Group Labeler window"""

    def __init__(self, dataset_path):
        """Initializes Group Labeler window object"""
        super(Impl_GroupLabelling_Window, self).__init__()
        self.setupUi(self)
        self.path = dataset_path
        self.pushButton.clicked.connect(self.displayMatchingRecordsfromfile)

        # Add items to the comboBox
        try:
            df = pd.read_csv(dataset_path)  # Use read_excel for Excel files
            column_names = df.columns
            self.comboBox.addItems(column_names)  # Add column names directly to the comboBox
            max_width = self.comboBox.view().sizeHintForColumn(0)
            self.comboBox.view().setMinimumWidth(max_width)
            self.comboBox.currentIndexChanged.connect(self.updateDropdownItems)  # Connect the event handler
        except Exception as e:
            print("Error:", e)
    
    def updateDropdownItems(self, index):
        """Update the dropdown with unique values from the selected column"""
        selected_column = self.comboBox.currentText()  # Get the selected column name
        if selected_column:
            try:
                df = pd.read_csv(self.path)
                unique_values = df[selected_column].unique()
                self.comboBox_2.clear()  # Clear the existing items
                self.comboBox_2.addItems([str(val) for val in unique_values])
                max_width = self.comboBox_2.view().sizeHintForColumn(0)
                self.comboBox_2.view().setMinimumWidth(max_width)

            except Exception as e:
                print("Error:", e)

    def displayMatchingRecordsfromfile(self):
        key = self.comboBox.currentText()
        value = self.comboBox_2.currentText()

        if key and value:
            try:
                df = pd.read_csv(self.path)
                matching_records = df[(df[key] == value)]
                num_columns = len(df.columns)

                # Clear previous content in the QTableWidget
                self.tbl_MatchingRecords.setRowCount(0)
                self.tbl_MatchingRecords.setColumnCount(num_columns+1)
                header_labels = df.columns.tolist() + ["Output"]
                self.tbl_MatchingRecords.setHorizontalHeaderLabels(header_labels)

                # Populate the QTableWidget with matching records
                for i, (_, row) in enumerate(matching_records.iterrows()):
                    self.tbl_MatchingRecords.insertRow(i)
                    for j, val in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(val))
                        self.tbl_MatchingRecords.setItem(i, j, item)
                    output_item = QtWidgets.QTableWidgetItem("Output Value")  # You can set the default output value here
                    self.tbl_MatchingRecords.setItem(i, num_columns, output_item)

            except Exception as e:
                print("Error:", e)

