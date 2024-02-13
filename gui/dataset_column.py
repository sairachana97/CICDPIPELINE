from typing import Any, List
import pandas as pd
import numpy as np
import os


class DatasetColumn:
    """Dataset Column class used to represent a column from either csv or xml datasets."""

    def __init__(
        self,
        name: str,
        data: str,
        training: bool,
        transformation: str,
        col_type: str,
        tp_label: str = "",
        t_params: dict = {},
    ) -> None:
        """Init method of DatasetColumn class

        Args:
            name (str): Name of column.
            data (str): Data type of column.
            training (bool): Whether or not this column should be used for training a model.
            transformation (str): Transformation to apply to column.
            col_type (str): Type of column.
            tp_label (str, optional): True positive label. Only set if col_type is output. Defaults to "".
            t_params (dict, optional): Transformation parameters, needed for numerical transformations. Defaults to {}.
        """
        self.Name = name
        self.Data = data
        self.Training = training
        self.Transformation = transformation
        self.Type = col_type
        self.TPLabel = tp_label
        self.Transformation_Params = t_params

    def __str__(self):
        """String representation of DatasetColumn.

        Returns:
            str: Representation of DatasetColumn object.
        """
        return """Name: {} Data: {} Training: {} Transformation: {} Type: {} TPLabel: {}""".format(
            self.Name, self.Data, self.Training, self.Transformation, self.Type, self.TPLabel
        )

    def fromdict(colDict):
        """Created a DatasetColumn object from a dictionary.

        Args:
            colDict (dict): Dictionary containing all required fields to create a DatasetColumn instance.

        Returns:
            DatasetColumn: DatasetColumn instance.
        """
        name_ = colDict["name"]
        data_ = colDict["data"]
        training_ = colDict["training"]
        transformation_ = colDict["transformation"]
        transformation_params = colDict["transformation_params"]
        type_ = colDict["type"]
        tplabel_ = colDict["tplabel"]

        return DatasetColumn(
            name_,
            data_,
            training_,
            transformation_,
            type_,
            tplabel_,
            transformation_params,
        )

    def asdict(self, dataframe: pd.DataFrame):
        """Represents a DatasetColumn object as a dictionary.

        Args:
            dataframe (pd.DataFrame): Pandas DataFrame containing the values of all columns.

        Returns:
            dict: Dictionary representation of DatasetColumn object.
        """
        unique = []
        num_unique = 0
        if self.Transformation == "Gaussian Dist":
            mean = np.mean(dataframe[self.Name].values)
            std = np.std(dataframe[self.Name].values)
            self.Transformation_Params = {"mean": mean, "std": std}
        elif self.Transformation == "Uniform Dist":
            _max = np.max(dataframe[self.Name].values)
            _min = np.min(dataframe[self.Name].values)
            self.Transformation_Params = {"max": _max, "min": _min}
        elif self.Transformation == "One-hot Encoding":
            #Storing mapping of one hot values.
            unique = sorted(dataframe[self.Name].apply(str).unique()) if self.Training else []
            num_unique = len(unique) if self.Training else 0


        return {
            "name": self.Name,
            "data": self.Data,
            "training": self.Training,
            "transformation": self.Transformation,
            "transformation_params": self.Transformation_Params,
            "type": self.Type,
            "tplabel": self.TPLabel,
            "unique": unique,
            "num_unique": num_unique,
        }

    def split_name_xml(self):
        """Splits string name by '->' separator

        Returns:
            list(str): Name as a list of strings
        """
        return self.Name.split("->")

    def CreateJson(
        dataset_columns: List[Any],
        filePath: str,
        trainSplit: int,
        dataframe: pd.DataFrame,
        xml_params=None,
    ):
        """Creates a json-dict representation of a list of dataset columns with extra parameters.

        Args:
            dataset_columns (List[Any]): List of dataset columns.
            filePath (str): Filename pointing to dataset.
            trainSplit (int): Percentage of dataset for training.
            dataframe (pd.DataFrame): Pandas DataFrame with all our data.
            xml_params (dict, optional): Extra parameters required for XML handling. Defaults to None.

        Returns:
            jsonDict(dict): Dictionary containing all schema fields.
        """
        outputColumn = [c for c in dataset_columns if c.Type == "Output"][0]
        cName = outputColumn.Name
        train_idx = dataframe.groupby(cName).apply(
            lambda x: x.sample(frac=trainSplit / 100.0, random_state=0)
        )
        train_idx = train_idx.drop(columns=[cName])
        train_idx = train_idx.reset_index(level=[0])
        train_idx = train_idx.index.values

        jsonDict = {
            "filename": filePath,
            "format": os.path.splitext(filePath)[1][1:].lower(),
            "xml_params": xml_params,
            "columns": [d.asdict(dataframe) for d in dataset_columns],
            "trainSplit": trainSplit,
            "testSplit": 100 - trainSplit,
            "trainIdx": train_idx.tolist(),
            "testIdx": list(
                set([i for i in range(dataframe.shape[0])]) - set(train_idx.tolist())
            ),
        }

        return jsonDict
    
    def CreateRiskJson(
        dataset_columns: List[Any],
        trainSplit: int,
        dataframe: pd.DataFrame,
        xml_params=None,
    ):
        """Creates a json-dict representation of a list of dataset columns with extra parameters.

        Args:
            dataset_columns (List[Any]): List of dataset columns.
            filePath (str): Filename pointing to dataset.
            trainSplit (int): Percentage of dataset for training.
            dataframe (pd.DataFrame): Pandas DataFrame with all our data.
            xml_params (dict, optional): Extra parameters required for XML handling. Defaults to None.

        Returns:
            jsonDict(dict): Dictionary containing all schema fields.
        """
        outputColumn = [c for c in dataset_columns if c.Type == "Output"][0]
        cName = outputColumn.Name
        train_idx = dataframe.groupby(cName).apply(
            lambda x: x.sample(frac=trainSplit / 100.0, random_state=0)
        )
        train_idx = train_idx.drop(columns=[cName])
        train_idx = train_idx.reset_index(level=[0])
        train_idx = train_idx.index.values

        jsonDict = {
            "format": "csv",
            "xml_params": xml_params,
            "columns": [d.asdict(dataframe) for d in dataset_columns],
            "trainSplit": trainSplit,
            "testSplit": 100 - trainSplit,
            "trainIdx": train_idx.tolist(),
            "testIdx": list(
                set([i for i in range(dataframe.shape[0])]) - set(train_idx.tolist())
            ),
        }

        return jsonDict
    
    def fromdict1(column):
        """Created a DatasetColumn object from a dictionary.

        Args:
            colDict (dict): Dictionary containing all required fields to create a DatasetColumn instance.

        Returns:
            DatasetColumn: DatasetColumn instance.
        """
        name_ = column
        data_ = "Categorical"
        training_ = "True"
        transformation_ = "One-hot Encoding"
        transformation_params = ""
        if(column == "@severity"):
            type_ = "Output"
            tplabel_ = "high"

        elif column != "Base Finding Score" or column != "Attack Surface Score" or column != "Environmental Score" or column != "Final Score"  or column != "risk_details":
            type_ = "Input"
            tplabel_ = ""

        return DatasetColumn(
            name_,
            data_,
            training_,
            transformation_,
            type_,
            tplabel_,
            transformation_params,
        )
