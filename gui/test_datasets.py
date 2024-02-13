import os
import pandas as pd
from datasets import Impl_DatasetsWindow
import unittest
import sys

from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

class Impl_DatasetsWindowTest(unittest.TestCase):
    '''Test the DatasetsWindow GUI'''
    def setUp(self):
        '''Create the GUI'''
        self.form = Impl_DatasetsWindow()
        self.test_csv_path = 'test.csv'
        self.test_csv_data = {'Fixable': [0, 1, 1], 'Column1': ['A', 'B', 'C'], 'Column2': [4.5, 6.7, 8.9]}
        self.test_df = pd.DataFrame(data=self.test_csv_data)
        self.test_json_data = {"@priority": ["1", "2", "3", "4", ""], "@Fixable": [0, 1, 0, 1, ""], "@status": ["false-positive", "false-positive", "false-positive", "false-positive", ""]}
        self.test_df = pd.DataFrame(self.test_json_data)

    def tearDown(self):
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_btn_Labeler_clicked(self):
        self.form.btn_Labeler_clicked()
        pass

    def test_btn_Labeler_clicked_fail(self):
        self.form.convertXmlToCSV("Test.xml")
        self.form.btn_Labeler_clicked("Test.csv")
        pass

    def test_checkFileFormat(self):
        self.assertEqual(self.form.checkFileFormat("Test.xml"), True)
        self.assertEqual(self.form.checkFileFormat("Test.csv"), False)
    
    def test_load_csv_dataset_file_fail(self):
        csv_path = self.test_csv_path
        self.assertFalse(os.path.exists(csv_path))

        # Call the function under test
        self.form.loadDatasetFile(csv_path)

        #Check that the function correctly loads the csv file
        self.assertTrue(os.path.exists(csv_path))
        self.assertEqual(self.form.dataset_type, 'csv')
        self.assertTrue('Status' in self.form.df_dataset.columns)
        self.assertEqual(self.form.df_dataset['Status'].iloc[0], 'false-positive')
        self.assertEqual(self.form.df_dataset['Status'].iloc[1], 'escalated')
        self.assertEqual(self.form.df_dataset['Status'].iloc[2], 'escalated')
        self.assertEqual(len(self.form.cBox_Preset), 20)

    def test_save_csv_dataset_file_fail(self):
        csv_path = self.test_csv_path
        self.form.dataset_type = 'csv'
        self.form.df_dataset = self.test_df

        # Call the function under test
        self.form.loadDatasetFile(csv_path)

        # Check that the function correctly saves the csv file
        self.assertTrue(os.path.exists(csv_path))
        saved_data = pd.read_csv(self.test_csv_path)
        self.assertTrue('Status' in saved_data.columns)
        self.assertEqual(saved_data['Status'].iloc[1], 'escalated')
        self.assertEqual(saved_data['Status'].iloc[2], 'escalated')
        self.assertEqual(len(self.form.cBox_Preset), 20)
    
    def test_PMD(self):
        df = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Priority': [2, 4, 3, 1]})
        # Check if 'Priority' column is present in the DataFrame
        assert 'Priority' in df.columns

        # Check if 'Status' column is not present in the DataFrame
        assert 'Status' not in df.columns

    def set_status_column_fail(df_dataset):
        # Helper function to apply the modifications to the @status column
        if not df_dataset.empty:
            if not df_dataset['@priority'].isna().all():
                df_dataset['@status'] = df_dataset['@priority']
                first_column = df_dataset.pop('@status')
                df_dataset.insert(0,'@status',first_column)
                df_dataset['@status'] = np.where(df_dataset['@status']>="3",'escalated','false-positive')
            elif not df_dataset['@Fixable'].isna().all():
                df_dataset['@status'] = df_dataset['@Fixable']
                first_column = df_dataset.pop('@status')
                df_dataset.insert(0,'@status',first_column)
                df_dataset['@status'] = df_dataset["@status"].replace(0,'false-positive')
                df_dataset['@status'] = df_dataset["@status"].replace(1,'escalated')
        return df_dataset
     

    
if __name__ == "__main__":
    unittest.main()