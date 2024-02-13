from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(1280, 720)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        HelpWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        HelpWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/ML4CYBER_Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        HelpWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(HelpWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QTextEdit(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 89, 1100, 500))
        self.label.setObjectName("label")
        self.label.setReadOnly(True)
        # 28-sep-2023
        self.label.setStyleSheet("background-color: #f0f0f0;")  # Set the background color
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 30, 1100, 50))
        self.label_2.setObjectName("label_2")
        HelpWindow.setCentralWidget(self.centralwidget)
       

        self.retranslateUi(HelpWindow)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)


    def retranslateUi(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        if(HelpWindow.type == "Main"):
            self.label_2.setText(_translate("HelpWindow", "<html><head/><body><b>Here is all the information about the tool!</b></body></html>"))
            self.label.setText(_translate("HelpWindow", """
                <html><head/><body>
                <ul>
                <li><b>Datasets:</b> This is the screen you would go if the user has only .xml file. Here we can convert it to .csv which is important to proceed further. In the same window, you can also label the dataset. More info can be found in Dataset Help screen.</li>
                <li><b>Risk:</b> This screen basically takes to second step where the user can import .csv and Save the scheme to train the model. More info found on Risk screen help button.</li>
                <li><b>Model Training:</b> The saved scheme is used to train the model. More info found on Models screen help button.</li>
                <li><b>Predictions:</b> This screen will predict the trained model about the vulnerabilities. The trained dataset is again used in the predictions to predict the accuracy of the model. More info found on Predictions screen help button.</li>
                </ul>
                </body></html>
            """))

        if(HelpWindow.type == "Labeler"):
            HelpWindow.setWindowTitle(_translate("HelpWindow", "Help | Vinci ML Tool"))
            self.label_2.setText(_translate("HelpWindow", "Here is all the information about the Labeler Window"))
            self.label.setText(_translate("HelpWindow", "You can separate here the training set. Load the dataset you saved as a .csv file before, select the Stratified type and save the training set.\nLoad the training dataset you just created at the Dataset Labeling section. Each finding will be displayed separately and you will be able to assign the True or False label using the check boxes on the right. Save the dataset and close the window."))    
            
        if(HelpWindow.type == "Risk"):
            self.label_2.setText(_translate("HelpWindow", "<html><head/><body><b>Here is all the information about the Risk window.</b></body></html>"))
            self.label.setText(_translate("HelpWindow", """
                <html><head/><body>
                The risk window can be used to assess the risk of the software vulnerabilities. The CWSS (Common Weakness Scoring System) Score is the ultimate score that evaluates the threat of the software vulnerabilities. The Base Finding Score, Attack Surface Score, and Environment Score add up to form the score of the threat. Several tabs in the window display the detailed description of each of the scores shown.
                </body></html>
            """))
        if(HelpWindow.type == "Prediction"):
            self.label_2.setText(_translate("HelpWindow", "<html><head/><body><b>Here is all the information about the Prediction window.</b></body></html>"))
            self.label.setText(_translate("HelpWindow", """
                <html><head/><body>
                Load the original dataset, the schema you created, and the training model. Press Predict and Save Results when finished to save a .csv file with the predictions.
                </body></html>
            """))

        if(HelpWindow.type == "Models"):
            self.label_2.setText(_translate("HelpWindow", "<html><head/><body><b>Here is all the information about the 'Models' window.</b></body></html>"))
            self.label.setText(_translate("HelpWindow", """
                <html><head/><body>
                The model window can be used to train the dataset. Load the schema you want to use for training. Set the epochs and learning rate. Also select the metrics you want to use. Click on Train Now to train the model and use Save Model to save the trained model to your system. The threshold can also be set, and metrics information can be viewed on the bottom section of the window.
                </body></html>
            """))
        if(HelpWindow.type == "Dataset"):
            self.label_2.setText(_translate("HelpWindow", "<html><head/><body><b>Here is all the information about the DataSet Window.</b></body></html>"))
            self.label.setText(_translate("HelpWindow", """
                <html><head/><body>
                Click the Datasets button, press the Load Dataset on the top left corner, and select the csv or xml file that contains the dataset. (It seems to work mostly with the XMLs; with the CSV, you have to manually pick the "preset" on the right). The tool will recognize the type of the report and preload the recommended features for best prediction accuracy.<br>
                You can add or remove columns and start labeling the dataset, which can also be saved to be used later.
                </body></html>
            """))
        if(HelpWindow.type == "Risk Model"):
            self.label_2.setText(_translate("HelpWindow", "<html><head/><body><b>Here is all the information about the 'Risk Model' window.</b></body></html>"))
            self.label.setText(_translate("HelpWindow", """
                <html><head/><body>
                The risk model window can be used to train the dataset. Load the schema which you want to use for training. Set the epochs and learning rate. Also select the metrics you want to use. Click on <b>Train Now</b> to train the model and use <b>Save Model</b> to save the trained model to your system. The threshold can also be set and metrics information can be viewed on the bottom section of the window.
                </body></html>
            """))
import menu_res_rc
