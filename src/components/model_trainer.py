"""Train and evaluate a transparent baseline default-risk classifier."""

from pathlib import Path
import sys

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_score, recall_score, roc_auc_score

from src.entity.config_entity import ModelTrainerConfig
from src.exception.exception import CreditRiskException
from src.utils.common import create_directories, save_json


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(self, train_path: Path, test_path: Path) -> Path:
        try:
            train_features, train_target = joblib.load(train_path)
            test_features, test_target = joblib.load(test_path)
            model = LogisticRegression(
                C=self.config.C,
                max_iter=self.config.max_iter,
                class_weight=self.config.class_weight,
                random_state=self.config.random_state,
                solver="saga",
            )
            model.fit(train_features, train_target)
            probabilities = model.predict_proba(test_features)[:, 1]
            predictions = (probabilities >= 0.5).astype(int)
            metrics = {
                "roc_auc": float(roc_auc_score(test_target, probabilities)),
                "average_precision": float(average_precision_score(test_target, probabilities)),
                "precision_at_0_5": float(precision_score(test_target, predictions, zero_division=0)),
                "recall_at_0_5": float(recall_score(test_target, predictions, zero_division=0)),
            }
            create_directories([self.config.root_dir])
            joblib.dump(model, self.config.model_path)
            save_json(Path(self.config.metrics_path), metrics)
            return Path(self.config.model_path)
        except Exception as error:
            raise CreditRiskException(error, sys) from error
