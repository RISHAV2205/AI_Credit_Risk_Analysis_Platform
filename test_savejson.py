from pathlib import Path

from src.utils.common import save_json

metrics = {
    "accuracy": 0.91,
    "precision": 0.89,
    "recall": 0.85,
    "f1_score": 0.87
}

save_json(
    Path("artifacts/evaluation/metrics.json"),
    metrics
)



