#!/usr/bin/env python3
"""CLI script for batch prediction on new customer data."""
import sys
import argparse
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_predict")


def main():
    parser = argparse.ArgumentParser(description="Run batch predictions on customer data")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--model", default="aegisxai/models/trained_model.pkl",
                        help="Path to trained model pickle")
    parser.add_argument("--output", default="predictions_output.csv",
                        help="Path for output CSV")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Probability threshold for churn classification")
    args = parser.parse_args()

    logger.info("Loading input data from %s", args.input)
    df = pd.read_csv(args.input)
    logger.info("Loaded %d rows", len(df))

    required_cols = ["tenure", "MonthlyCharges", "Contract", "InternetService"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        logger.error("Missing required columns: %s", missing)
        return 1

    logger.info("Loading model from %s", args.model)
    import joblib
    model = joblib.load(args.model)

    from aegisxai.models.features import engineer_features
    df_feat = engineer_features(df)

    predict_cols = [c for c in df_feat.columns if c not in ("Churn", "customerID")]
    X = df_feat[predict_cols]
    X = X.select_dtypes(include=[np.number])

    missing_model_cols = set(model.feature_names_in_) - set(X.columns)
    if missing_model_cols:
        for c in missing_model_cols:
            X[c] = 0
    X = X[model.feature_names_in_]

    logger.info("Running predictions on %d rows...", len(X))
    y_prob = model.predict_proba(X)[:, 1]
    y_pred = (y_prob >= args.threshold).astype(int)

    results = df[["customerID"]].copy() if "customerID" in df.columns else pd.DataFrame()
    results["churn_probability"] = np.round(y_prob, 4)
    results["prediction"] = np.where(y_pred == 1, "Churn", "Retain")
    results["risk_level"] = pd.cut(
        y_prob,
        bins=[0, 0.3, 0.6, 1.0],
        labels=["Low", "Medium", "High"]
    )

    results.to_csv(args.output, index=False)
    logger.info("Predictions saved to %s", args.output)

    risk_counts = results["risk_level"].value_counts()
    logger.info("Risk distribution: %s", risk_counts.to_dict())
    logger.info("Predicted churn rate: %.1f%%", results["prediction"].eq("Churn").mean() * 100)

    return 0


if __name__ == "__main__":
    sys.exit(main())
