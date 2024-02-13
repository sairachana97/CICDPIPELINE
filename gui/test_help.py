from help import Impl_HelpWindow
import unittest
import sys

from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

class Impl_HelpWindowTest(unittest.TestCase):
    '''Test the HelpWindow GUI'''
    def setUp(self):
        '''Create the GUI'''
        self.form = Impl_HelpWindow(type)

    def test_customInit(self):
        self.form.customInit()
        pass

    def test_LandingScreenHelp(self):
        self.form.type = "Main"
        self.form.label.setText("Testing")
        self.assertNotEqual(self.form.label.toPlainText(), 
        "The three Buttons are used to Load the Datasets,"
        + " Train and then Predict the trained model about"
        + " the vulnerablities. Datasets Button redirects to"
        + " the Dataset window which is mostly used to load"
        + " the Dataset which is the output of the static code"
        + " analyser. In the same window you can also label the"
        + " dataset. After labelling the dataset you will be"
        + " training the dataset by loading the schema and"
        + " selecting approapriate things to save the dataset."
        + " The trained dataset is again used in the predictions"
        + " to predict the accuracy of the model.")

    def test_labelerHelp(self):
        self.form.type = "Labeller"
        self.form.label.setText("Testing")
        self.assertNotEqual(self.form.label.toPlainText(), 
        "You can separate here the training set. Load the"
        + " dataset you saved as a .csv file before, select"
        + " the Stratified type and save the training set.\nLoad"
        + " the training dataset you just created at the Dataset"
        + " Labeling section. Each finding will be displayed separately"
        + " and you will be able to assign the True or False label using"
        + " the check boxes on the right. Save the dataset and close the window.")

    def test_riskHelp(self):
        self.form.type = "Risk"
        self.form.label.setText("Testing")
        self.assertNotEqual(self.form.label.toPlainText(),
        "The risk window can be used to assess the risk of the software vulnerabilities." 
        + " The CWSS(Common Weakness Scoring System) Score is the ultimate score which evaluates" 
        + " the threat of the software vulnerabilities. The Base Finding Score, Attack Surface Score," 
        + "and Environment Score add up to form the score of the threat. Several tabs in the window" 
        + " display the detailed description of each of the scores shown. ")

    def test_PredictionHelp(self):
        self.form.type = "Prediction"
        self.form.label.setText("Testing")
        self.assertNotEqual(self.form.label.toPlainText(),
        "Load the original dataset, the schema you created and the training model." 
        + " Press Predict and Save Results when finished to save a .csv file with the predictions.")

    def test_RiskModelHelp(self):
        self.form.type = "Risk Model"
        self.form.label.setText("Testing")
        self.assertNotEqual(self.form.label.toPlainText(),
        "The risk model window can be used to train the dataset."
        + " Load the schema which you want to use for training." 
        + " Set the epochs and learning rate. Also select the metrics you want to use." 
        + " Click on Train Now to train the model and use Save Model to save the trained"
        + " model to your system. The threshold can also be set and metrics information can" 
        + " be viewed on the bottom section of the window.")


if __name__ == "__main__":
    unittest.main()