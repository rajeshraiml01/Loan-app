import pandas as pd

from loan_app.config import DATA_PATH, MODEL_FEATURES, TARGET_COLUMN


def load_dataset(path=DATA_PATH) -> pd.DataFrame:
    """Load training data from CSV."""
    return pd.read_csv(path)


def split_features_target(df: pd.DataFrame):
    """Return feature matrix and target series with stable column order."""
    x = df[MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].astype(int)
    return x, y
