from models import Impl_ModelsWindow

import sys
import unittest
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

class ModelUITest(unittest.TestCase):
    def setUp(self):
        """Define initial setup"""
        self.ui = Impl_ModelsWindow()

    def test_epochsBox(self):
        """Test the Epochs box tooltip"""
        self.assertEqual(self.ui.sBox_Epochs.toolTip(), "Number of complete passes a training dataset takes through the algorithm.")

    def test_learningRateBox(self):
        """Test the Learning Rate box tooltip"""
        self.assertEqual(self.ui.txtB_LearningRate.toolTip(), "The speed at which an algorithm learns the values of a parameter estimate. Optimal range - 0.0 to 1.0")

    def test_accuracyBox(self):
        """Test the Accuracy metric box tooltip"""
        self.assertEqual(self.ui.cBox_MetricsAccuracy.toolTip(), "The measure of how often the algorithm is predicting correctly.")

    def test_precisionBox(self):
        """Test the Precision metric box tooltip"""
        self.assertEqual(self.ui.cBox_MetricsPrecision.toolTip(), "Measure of relevant data from model's predictions.")

    def test_recallBox(self):
        """Test the Recall metric box tooltip"""
        self.assertEqual(self.ui.cBox_MetricsRecall.toolTip(), "Measures the model's ability to detect positive samples.")

    def test_trainSampleBox(self):
        """Test the Train Samples metric box tooltip"""
        self.assertEqual(self.ui.txtB_InfoTrainSamples.toolTip(), "Number of training samples in the dataset.")

    def test_testSampleBox(self):
        """Test the Test Samples metric box tooltip"""
        self.assertEqual(self.ui.txtB_InfoTestSamples.toolTip(), "Number of test samples in the dataset.")

    def test_infoFeaturesBox(self):
        """Test the Info Features metric box tooltip"""
        self.assertEqual(self.ui.txtB_InfoFeatures.toolTip(), "Number of features in the dataset.")

    def test_trainProgressBox(self):
        """Test the Train Progress metric box tooltip"""
        self.assertEqual(self.ui.pBar_TrainProgress.toolTip(), "Progress of model training.")
    
    def test_TPBox(self):
        """Test the True Positive metric box tooltip"""
        self.assertEqual(self.ui.txtB_EvalMetricsTP.toolTip(), "Outcome where model correctly predicts the positive result.")
    
    def test_TNBox(self):
        """Test the True Negative metric box tooltip"""
        self.assertEqual(self.ui.txtB_EvalMetricsTN.toolTip(), "Outcome where model correctly predicts the negative result.")

    def test_FPBox(self):
        """Test the False Positive metric box tooltip"""
        self.assertEqual(self.ui.txtB_EvalMetricsFP.toolTip(), "Outcome where model incorrectly predicts the positive result.")

    def test_FNBox(self):
        """Test the False Negative metric box tooltip"""
        self.assertEqual(self.ui.txtB_EvalMetricsFN.toolTip(), "Outcome where model incorrectly predicts the negative result.")

    def test_f1ScoreBox(self):
        """Test the F1 Score metric box tooltip"""
        self.assertEqual(self.ui.txtB_EvalMetricsF1.toolTip(), "Measure of a model's accuracy on a dataset.")

    def test_lossBox(self):
        """Test the Loss box tooltip"""
        self.assertEqual(self.ui.txtB_EvalMetricsLoss.toolTip(), "Errors made by the model for each sample.")

    def test_thresholdBox(self):
        """Test the Threshold box tooltip"""
        self.assertEqual(self.ui.dsBox_Threshold.toolTip(), "Helps map a logistic regression value to binary value. Optimal value - 0.50")

if __name__ == "__main__":
    unittest.main()