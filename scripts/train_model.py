#!/usr/bin/env python3
"""CLI script to train/retrain the XGBoost churn model from scratch."""
import sys
import argparse
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("train_model")


def main():
    parser = argparse.ArgumentParser(description="Train AegisXAI churn prediction model")
    parser.add_argument("--data", default="aegisxai/data/WA_Fn-UseC_-Telco-Customer-Churn.csv",
                        help="Path to churn CSV")
    parser.add_argument("--output", default="aegisxai/models/trained_model.pkl",
                        help="Output path for trained model")
    parser.add_argument("--trials", type=int, default=20,
                        help="Number of Optuna trials")
    parser.add_argument("--test-size", type=float, default=0.2,
                        help="Test set proportion")
    args = parser.parse_args()

    logger.info("Loading data from %s", args.data)
    from aegisxai.models.features import load_data, engineer_features
    df = load_data(args.data)
    logger.info("Loaded %d rows", len(df))

    df = engineer_features(df)
    logger.info("Engineered features: %d columns", len(df.columns))

    X = df.drop(columns=["Churn", "customerID"], errors="ignore")
    y = (df["Churn"] == "Yes").astype(int)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )

    logger.info("Training XGBoost with Optuna (%d trials)...", args.trials)
    from aegisxai.models.train import train_model
    model, study = train_model(X_train, y_train, n_trials=args.trials)

    from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    acc = accuracy_score(y_test, y_pred)

    logger.info("ROC-AUC: %.4f", auc)
    logger.info("Accuracy: %.4f", acc)
    logger.info("\n" + classification_report(y_test, y_pred))

    import joblib
    joblib.dump(model, args.output)
    logger.info("Model saved to %s", args.output)

    from aegisxai.models.registry import init_registry
    registry = init_registry()
    registry.append({
        "version": f"v4.{datetime.now().strftime('%Y%m%d')}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "algorithm": "XGBoost+Optuna",
        "roc_auc": round(auc, 3),
        "accuracy": round(acc, 3),
        "status": "Active",
    })
    logger.info("Registry updated — version: v4.%s", datetime.now().strftime('%Y%m%d'))

    return 0


if __name__ == "__main__":
    sys.exit(main())
