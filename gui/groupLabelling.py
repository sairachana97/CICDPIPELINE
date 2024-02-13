import pandas as pd
from groupLabelling_ui import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QInputDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal

class Impl_GroupLabelling_Window(Ui_Dialog, QtWidgets.QMainWindow):
    """Creates Group Labeler window"""

    def __init__(self, dataset_path):
        """Initializes Group Labeler window object"""
        super(Impl_GroupLabelling_Window, self).__init__()
        self.setupUi(self)
        self.path = dataset_path
        self.displayed_records_df = pd.DataFrame()
        self.labeled_records = {}
        self.go_back_button.triggered.connect(self.goback_button_clicked)
        self.home_button.triggered.connect(self.home_button_clicked)

        # Add items to the comboBox
        try:
            df = pd.read_csv(dataset_path)  # Use read_excel for Excel files
            column_names = df.columns
            self.comboBox.addItems(column_names)  # Add column names directly to the comboBox
            max_width = self.comboBox.view().sizeHintForColumn(0)
            self.comboBox.view().setMinimumWidth(max_width)
            self.comboBox.currentIndexChanged.connect(self.displayMatchingRecords)
            self.comboBox_2.currentIndexChanged.connect(self.displayMatchingRecords)
        
            self.comboBox.currentIndexChanged.connect(self.updateDropdownItems)
              # Connect the event handler
        except Exception as e:
            print("Error:", e)
        
        self.pushButton.clicked.connect(self.labelRecords)
        self.save_dataset_button.clicked.connect(self.saveDataset)
        

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

    def displayMatchingRecords(self):
        key = self.comboBox.currentText()
        value = self.comboBox_2.currentText()

        if key and value:
            try:
                df = pd.read_csv(self.path)
                matching_records = df[df[key] == value]

                # Clear previous content in the QTableWidget by setting row count to 0
                self.tbl_MatchingRecords.setRowCount(0)

                num_columns = len(df.columns)

                # Check if the "Output" column already exists in the original CSV file
                if "Output" not in df.columns:
                    # Add the "Output" column to the DataFrame and initialize it with None
                    df["Output"] = None
                    num_columns += 1  # Increment the column count

                # Set up the QTableWidget with the correct number of columns
                self.tbl_MatchingRecords.setColumnCount(num_columns + 1)
                header_labels = ['Number'] + df.columns.tolist()
                self.tbl_MatchingRecords.setHorizontalHeaderLabels(header_labels)
                self.tbl_MatchingRecords.verticalHeader().setVisible(False)


                # Populate the QTableWidget with matching records, including original row numbers
                for i, (original_row_number, row) in enumerate(matching_records.iterrows(), start=1):
                    self.tbl_MatchingRecords.insertRow(i - 1)
                    # Display the original row number in the first column
                    item = QtWidgets.QTableWidgetItem(str(original_row_number + 1))
                    self.tbl_MatchingRecords.setItem(i - 1, 0, item)
                    for j, val in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(val))
                        self.tbl_MatchingRecords.setItem(i - 1, j + 1, item)
                    # Set the "Output" column to its actual value if it exists, or None otherwise
                    output_value = row.get("Output", None)
                    if output_value is not None:
                        output_item = QtWidgets.QTableWidgetItem(str(output_value))
                    else:
                        output_item = QtWidgets.QTableWidgetItem("None")
                    self.tbl_MatchingRecords.setItem(i - 1, num_columns, output_item)

            except Exception as e:
                print("Error:", e)


    def labelRecords(self):
        # This method is called when the "Label" button is clicked.

        # Check if a label has been selected
        if not self.true_radio_button.isChecked() and \
        not self.false_radio_button.isChecked() and \
        not self.clear_button.isChecked():
            # None of the radio buttons are selected, show an error message
            QMessageBox.critical(self, "Error", "Please select a label (True/False/None).")
            return

        # Get the selected label
        if self.true_radio_button.isChecked():
            label_value = "True"
        elif self.false_radio_button.isChecked():
            label_value = "False"
        elif self.clear_button.isChecked():
            label_value = "None"

        # Get the selected key and value
        key = self.comboBox.currentText()
        value = self.comboBox_2.currentText()

        if key and value:
            # Update both the QTableWidget and the labeled_records dictionary
            for row_index in range(self.tbl_MatchingRecords.rowCount()):
                number_item = self.tbl_MatchingRecords.item(row_index, 0)
                if number_item is not None:
                    original_row_number = int(number_item.text())
                    # Update the QTableWidget
                    output_item = self.tbl_MatchingRecords.item(row_index, self.tbl_MatchingRecords.columnCount() - 1)
                    if output_item is not None:
                        output_item.setText(label_value)
                    else:
                        output_item = QTableWidgetItem(label_value)
                        self.tbl_MatchingRecords.setItem(row_index, self.tbl_MatchingRecords.columnCount() - 1, output_item)

                    # Update the labeled_records dictionary
                    self.labeled_records[original_row_number] = label_value

            # Inform the user that the labels have been applied
            QMessageBox.information(self, "Info", "Labels applied to displayed records.")

    # Modify the saveDataset method
    def saveDataset(self):
    # Show a confirmation dialog before saving the dataset
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to save the dataset?")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.No)

        # User's choice
        user_choice = confirm_dialog.exec_()

        if user_choice == QMessageBox.Yes:
            # Get the path to save the updated dataset
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Dataset", "", "CSV Files (*.csv)")
            # self.path = save_path

            if save_path:
                try:
                    # Read the original dataset
                    original_df = pd.read_csv(self.path)

                    # Add 'risk_level' column if not already present
                    if 'risk_level' not in original_df.columns:
                        original_df['risk_level'] = ''

                    # Create a copy of the original dataset to store labeled records
                    labeled_df = original_df.copy()

                    # Apply labels to the copy based on the labeled_records dictionary
                    for row_number, label_value in self.labeled_records.items():
                        labeled_df.at[row_number - 1, "Output"] = label_value

                    # Save the labeled dataset as a new CSV file
                    labeled_df.to_csv(save_path, index=False)

                    self.path = save_path

                    # Display the saved file path
                    QMessageBox.information(self, "Info", f"Labeled dataset saved to: {save_path}")

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error while saving dataset: {e}")

            else:
                # If the user cancels, do nothing
                return

            
    # def goToLabeller(self):
    #     self.close()

    def goback_button_clicked(self):
        from datasets_labeler import Impl_DatasetsLabelerWindow
        self.bw_ui = Impl_DatasetsLabelerWindow(self.path)
        self.bw_ui.show()
        self.close()

    def home_button_clicked(self):
        from menu import Impl_MainWindow
        self.hm_ui = Impl_MainWindow()
        self.hm_ui.show()
        self.close()


