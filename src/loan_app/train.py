import argparse
import json
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split
from loan_app.config import (
    ARTIFACTS_DIR,
    CONFUSION_MATRIX_PATH,
    DATA_PATH,
    METRICS_PATH,
    MODELS_DIR,
    MODEL_PATH,
    RANDOM_STATE,
    ROC_FIGURE_PATH,
    TEST_SIZE,
)
from loan_app.data import load_dataset, split_features_target
from loan_app.evaluation import (
    classification_metrics,
    find_optimal_threshold,
    plot_confusion_matrix,
    plot_roc_curve,
    save_json,
)
from loan_app.modeling import build_pipeline, get_classifier_specs


def train(data_path: Path = DATA_PATH) -> dict:
    df = load_dataset(data_path)
    x, y = split_features_target(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model_name = "XGBClassifier"
    classifier = get_classifier_specs()[model_name]
    pipeline = build_pipeline(classifier)
    pipeline.fit(x_train, y_train)

    y_prob = pipeline.predict_proba(x_test)[:, 1]
    threshold_info = find_optimal_threshold(y_test, y_prob)
    threshold = threshold_info["threshold"]
    metrics = classification_metrics(y_test, y_prob, threshold)

    plot_roc_curve(y_test, y_prob, ROC_FIGURE_PATH)
    plot_confusion_matrix(y_test, y_prob, threshold, CONFUSION_MATRIX_PATH)

    joblib.dump(
        {
            "model": pipeline,
            "threshold": threshold,
            "model_name": model_name,
        },
        MODEL_PATH,
    )

    report = {
        "model": model_name,
        "metrics": metrics,
        "optimal_threshold": threshold_info,
    }
    save_json(METRICS_PATH, report)

    output = {
        "model": model_name,
        "model_path": str(MODEL_PATH),
        "metrics_path": str(METRICS_PATH),
        "roc_curve_path": str(ROC_FIGURE_PATH),
        "confusion_matrix_path": str(CONFUSION_MATRIX_PATH),
        "metrics": metrics,
        "threshold": threshold,
    }

    print(json.dumps(output, indent=2))
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train loan classifier and save best model")
    parser.add_argument("--data-path", default=str(DATA_PATH), help="Path to loan_data.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train(Path(args.data_path))


if __name__ == "__main__":
    main()
