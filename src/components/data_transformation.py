"""Fit a leakage-safe preprocessing pipeline and persist transformed datasets."""

from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.entity.config_entity import DataTransformationConfig
from src.exception.exception import CreditRiskException
from src.utils.common import create_directories


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def initiate_data_transformation(self, train_path: Path, test_path: Path):
        try:
            train_df, test_df = pd.read_csv(train_path), pd.read_csv(test_path)
            feature_columns = [
                column for column in train_df.columns
                if column not in {self.config.target_column, self.config.identifier_column}
            ]
            numeric_columns = train_df[feature_columns].select_dtypes(include="number").columns.tolist()
            categorical_columns = [column for column in feature_columns if column not in numeric_columns]
            preprocessor = ColumnTransformer(
                transformers=[
                    ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_columns),
                    ("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))]), categorical_columns),
                ],
                remainder="drop",
            )
            train_features = preprocessor.fit_transform(train_df[feature_columns])
            test_features = preprocessor.transform(test_df[feature_columns])
            create_directories([self.config.root_dir])
            joblib.dump(preprocessor, self.config.preprocessor_path)
            joblib.dump((train_features, train_df[self.config.target_column].to_numpy()), self.config.train_data_path)
            joblib.dump((test_features, test_df[self.config.target_column].to_numpy()), self.config.test_data_path)
            return Path(self.config.train_data_path), Path(self.config.test_data_path)
        except Exception as error:
            raise CreditRiskException(error, sys) from error
