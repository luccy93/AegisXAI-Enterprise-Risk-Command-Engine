import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def _compute_metrics(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
    }


def train_xgboost_model(X_train, y_train, X_test=None, y_test=None):
    from xgboost import XGBClassifier

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)
    metrics = {}
    if X_test is not None and y_test is not None:
        metrics = _compute_metrics(model, X_test, y_test)
    return model, metrics


def train_lightgbm_model(X_train, y_train, X_test=None, y_test=None):
    from lightgbm import LGBMClassifier

    model = LGBMClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1,
    )
    model.fit(X_train, y_train)
    metrics = {}
    if X_test is not None and y_test is not None:
        metrics = _compute_metrics(model, X_test, y_test)
    return model, metrics


def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    try:
        import streamlit as st
    except ImportError:
        return joblib.load(path)

    @st.cache_resource
    def _load(path_):
        return joblib.load(path_)

    return _load(path)
