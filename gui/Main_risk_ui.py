from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QLabel, QLineEdit, QFormLayout, QTabWidget, QGroupBox, QTableWidgetItem

class RiskWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Risk Window')
        self.setMinimumSize(1280, 720)

        # Create a vertical layout for the central widget
        central_layout = QVBoxLayout()

        # Set up Load Dataset layout
        self.setupLoadDatasetLayout(central_layout)

        # Set up Sample Info and Attack Surface layouts
        self.setupTabsLayout(central_layout)

        # Set the central layout for the main window
        self.setLayout(central_layout) 

    def setupLoadDatasetLayout(self, layout):
        # Create a horizontal layout for "Load Dataset" and "File Path"
        load_dataset_layout = QHBoxLayout()

        # Create a button named "Load Dataset"
        load_dataset_button = QtWidgets.QPushButton(self)
        load_dataset_button.setText("Load Dataset")
        load_dataset_button.clicked.connect(self.btn_Load_Dataset_clicked)

        # Create a QLabel to display the label "File Path:"
        file_path_label = QtWidgets.QLabel(self)
        file_path_label.setText("Path:")

        # Calculate the width for the file path line edit
        line_edit_width = self.width() - 320

        # Create a line edit widget to display the file path
        file_path_lineedit = QtWidgets.QLineEdit(self)
        file_path_lineedit.setPlaceholderText('Selected file path')
        file_path_lineedit.setReadOnly(True)

        # Add widgets for "Load Dataset" and "File Path" to the horizontal layout
        load_dataset_layout.addWidget(load_dataset_button)
        load_dataset_layout.addWidget(file_path_label)
        load_dataset_layout.addWidget(file_path_lineedit)

        # Create a group box for "Current Score" with a vertical layout
        current_score_group = QGroupBox("Current Score")
        current_score_layout = QVBoxLayout()

        # Create labels and placeholders for subscores and threat level
        subscore_labels = [
            "Base Finding Subscore:",
            "Environmental Subscore:",
            "Threat Level:",
            "Attack Surface Subscore:",
            "Final CWSS Score:"
        ]

        for label_text in subscore_labels:
            label = QtWidgets.QLabel(self)
            label.setText(label_text)
            label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            value_label = QtWidgets.QLabel(self)
            value_label.setText("0")  # Initialize the value to 0
            value_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            # Add labels and value labels to the vertical layout inside the group box
            current_score_layout.addWidget(label)
            current_score_layout.addWidget(value_label)

        # Set the layout of the group box to the vertical layout
        current_score_group.setLayout(current_score_layout)

        # Add the horizontal layout for "Load Dataset" and "File Path" and the group box to the main layout
        layout.addLayout(load_dataset_layout)
        layout.addWidget(current_score_group)

    def currentScoreLayout(self,layout):

        # Create a group box for "Current Score" with a vertical layout
        current_score_group = QGroupBox("Current Score")
        current_score_layout = QVBoxLayout()

        # Create labels and placeholders for subscores and threat level
        subscore_labels = [
            "Base Finding Subscore:",
            "Environmental Subscore:",
            "Threat Level:",
            "Attack Surface Subscore:",
            "Final CWSS Score:"
        ]

        for label_text in subscore_labels:
            label = QtWidgets.QLabel(self)
            label.setText(label_text)
            label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            value_label = QtWidgets.QLabel(self)
            value_label.setText("0")  # Initialize the value to 0
            value_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            # Add labels and value labels to the vertical layout inside the group box
            current_score_layout.addWidget(label)
            current_score_layout.addWidget(value_label)

        # Set the layout of the group box to the vertical layout
        current_score_group.setLayout(current_score_layout)

        # Add the horizontal layout for "Load Dataset" and "File Path" and the group box to the main layout
        layout.addWidget(current_score_group)



    def setupTabsLayout(self,layout):
        # Creating the tab widget
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(20, 200, 981, 500)

        # Call the functions to set up the Sample Info and Attack Surface tabs
        self.setupSampleInfoTab()
        self.setupAttackSurfaceTab()
        self.setupBaseFindingTab()
        self.setupEnvironmentalTab()

        # Add the tabWidget to the central layout
        layout.addWidget(self.tabWidget)

    def setupSampleInfoTab(self):
        # Sample Info tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "Sample Info")

        # Layout for Sample Info tab
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")

        # Group box for sample information
        self.group_box = QtWidgets.QGroupBox("Group Labelling", self.tab)
        self.group_box_layout = QVBoxLayout()
        self.group_box.setLayout(self.group_box_layout)

        # Adding labels and input fields for Sample Info inside the group box
        self.label_2 = QtWidgets.QLabel("Label 1:", self.tab)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)

        self.group_box_layout.addWidget(self.label_2)
        self.group_box_layout.addWidget(self.lineEdit_2)

        # Add the group box to the vertical layout
        self.verticalLayout.addWidget(self.group_box)

    def setupAttackSurfaceTab(self):
        # Attack Surface tab without the inside block for brevity
        self.attack_surface_tab = QWidget()
        self.attack_surface_tab.setObjectName("attack_surface_tab")
        self.tabWidget.addTab(self.attack_surface_tab, "Attack Surface")

        self.verticalLayout_attack_surface = QVBoxLayout(self.attack_surface_tab)
        self.verticalLayout_attack_surface.setObjectName("verticalLayout_attack_surface")

    def setupBaseFindingTab(self):
        # Attack Surface tab without the inside block for brevity
        self.base_finding_tab = QWidget()
        self.base_finding_tab.setObjectName("base_finding_tab")
        self.tabWidget.addTab(self.base_finding_tab, "Base Finding")

        self.verticalLayout_base_finding = QVBoxLayout(self.base_finding_tab)
        self.verticalLayout_base_finding.setObjectName("verticalLayout_base_finding")

        # Create the table widget without row and column headers
        self.table_base_finding = QTableWidget(5, 5)  # 5 rows, 5 columns
        self.table_base_finding.setHorizontalHeaderLabels(["", "", "", "", ""])  # Empty headers

        # Disable editing for all cells in the table
        for i in range(self.table_base_finding.rowCount()):
            for j in range(self.table_base_finding.columnCount()):
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table_base_finding.setItem(i, j, item)

        self.verticalLayout_base_finding.addWidget(self.table_base_finding)


    def setupEnvironmentalTab(self):
        self.environmental_tab = QWidget()
        self.environmental_tab.setObjectName("environmental_tab")
        self.tabWidget.addTab(self.environmental_tab, "Environmental")

        self.verticalLayout_environmental = QVBoxLayout(self.environmental_tab)
        self.verticalLayout_environmental.setObjectName("verticalLayout_environmental")



    def btn_Load_Dataset_clicked(self):
        """Clicked event on the Load Dataset button.
        Opens a file dialog to select a data file.
        """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Data File', '', 'CSV Files (*.csv);;XML Files (*.xml)')

        if file_path:
            print('Selected file:', file_path)
            # Update the line edit with the selected file path
            self.file_path_lineedit.setText(file_path)
            # Implement the logic to process the selected data file here
            # You can use the file_path to access the selected data file


