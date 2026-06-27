import numpy as np
import pandas as pd


def get_shap_explanation(model, X_test, idx):
    try:
        import shap

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        instance = X_test[idx : idx + 1]
        instance_sv = shap_values[idx]

        features = []
        for i in range(len(instance_sv)):
            features.append(
                {
                    "feature": f"Feature_{i}",
                    "value": round(float(instance[0, i]), 4),
                    "shap_value": round(float(instance_sv[i]), 4),
                }
            )
        features.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        return {
            "base_value": round(float(explainer.expected_value), 4),
            "features": features[:10],
            "prediction": "Churn" if np.mean(instance_sv) + explainer.expected_value > 0 else "No Churn",
        }
    except ImportError:
        return {"error": "SHAP not installed. See app.py for full implementation."}


def get_lime_explanation(model, X_train, X_test_idx, feature_names):
    try:
        import lime
        import lime.lime_tabular

        explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train,
            feature_names=feature_names,
            class_names=["No Churn", "Churn"],
            mode="classification",
            random_state=42,
        )
        exp = explainer.explain_instance(
            X_test_idx, model.predict_proba, num_features=10
        )
        return {
            "feature_weights": [
                {"feature": f, "weight": round(w, 4)}
                for f, w in exp.as_list()
            ],
            "prediction": "Churn" if model.predict([X_test_idx])[0] == 1 else "No Churn",
        }
    except ImportError:
        return {"error": "LIME not installed. See app.py for full implementation."}


def get_feature_importance(model, feature_names):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        return pd.DataFrame({"feature": feature_names, "importance": 0})

    df = pd.DataFrame({"feature": feature_names, "importance": importances})
    df = df.sort_values("importance", ascending=False).reset_index(drop=True)
    df["importance_pct"] = round(df["importance"] / df["importance"].sum() * 100, 2)
    return df


def get_counterfactual(model, instance, feature_names, target_class=0):
    cf = instance.copy()
    max_iter = 100
    step = 0.1
    for iteration in range(max_iter):
        pred = model.predict([cf])[0]
        if pred == target_class:
            break
        probas = model.predict_proba([cf])[0]
        direction = target_class - pred
        for j in range(len(cf)):
            perturbation = direction * step * (1 - probas[pred])
            cf[j] += perturbation
    changes = []
    for i, (orig, new) in enumerate(zip(instance, cf)):
        if abs(orig - new) > 0.01:
            changes.append(
                {
                    "feature": feature_names[i] if i < len(feature_names) else f"Feature_{i}",
                    "original": round(float(orig), 4),
                    "counterfactual": round(float(new), 4),
                    "change": round(float(new - orig), 4),
                }
            )
    return {
        "success": bool(model.predict([cf])[0] == target_class),
        "counterfactual_instance": cf.tolist(),
        "changes": changes[:10],
        "target_class": target_class,
    }
