from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from loan_app.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, RANDOM_STATE


def build_preprocessor() -> ColumnTransformer:
    """Build shared preprocessing for all classifiers."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def get_classifier_specs() -> dict:
    """Return the initialized classifier specs used by training."""
    return {
        "XGBClassifier": xgb.XGBClassifier(          
            random_state=RANDOM_STATE,
            eval_metric='logloss',
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            n_jobs=-1
        ),
    }


def build_pipeline(classifier) -> Pipeline:
    """Build a preprocessing + classification pipeline for a given estimator."""
    preprocessor = build_preprocessor()

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )
