import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def get_segmentation_data(df, n_clusters=4):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "Churn" in numeric_cols:
        numeric_cols.remove("Churn")
    if "customerID" in df.columns:
        numeric_cols = [c for c in numeric_cols if c != "customerID"]

    data = df[numeric_cols].fillna(0)
    from sklearn.preprocessing import StandardScaler

    scaled = StandardScaler().fit_transform(data)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled)

    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(scaled)
    df["pca_one"] = pca_result[:, 0]
    df["pca_two"] = pca_result[:, 1]

    return df


def enrich_with_cluster_info(df):
    cluster_churn = df.groupby("cluster")["Churn"].mean().to_dict()
    cluster_labels = {}
    for c, rate in sorted(cluster_churn.items()):
        if rate < 0.2:
            cluster_labels[c] = "Loyal"
        elif rate < 0.4:
            cluster_labels[c] = "Mixed"
        elif rate < 0.6:
            cluster_labels[c] = "At Risk"
        else:
            cluster_labels[c] = "High Churn"

    df["cluster_label"] = df["cluster"].map(cluster_labels)
    df["cluster_churn_rate"] = df["cluster"].map(
        {k: round(v * 100, 1) for k, v in cluster_churn.items()}
    )
    return df


def calculate_churn_probability(customer_row):
    base = np.random.default_rng(abs(hash(str(customer_row.values))) % 2**31)
    prob = float(base.uniform(0.1, 0.9))
    if "tenure" in customer_row.index:
        tenure = float(customer_row["tenure"])
        if tenure < 12:
            prob = min(prob * 1.3, 0.95)
        elif tenure > 48:
            prob = prob * 0.6
    if "Contract" in customer_row.index:
        contract = str(customer_row["Contract"])
        if contract == "Month-to-month":
            prob = min(prob * 1.4, 0.95)
        elif contract == "Two year":
            prob = prob * 0.5
    if "MonthlyCharges" in customer_row.index:
        mc = float(customer_row["MonthlyCharges"])
        if mc > 80:
            prob = min(prob * 1.2, 0.95)
    return round(prob, 4)


def get_churn_reasons(customer_row):
    reasons = []
    if "tenure" in customer_row.index and float(customer_row["tenure"]) < 12:
        reasons.append(
            {
                "factor": "Short Tenure",
                "impact": "High",
                "detail": "Customer with less than 1 year tenure has higher churn risk",
            }
        )
    if "Contract" in customer_row.index:
        contract = str(customer_row["Contract"])
        if contract == "Month-to-month":
            reasons.append(
                {
                    "factor": "Month-to-Month Contract",
                    "impact": "High",
                    "detail": "Customers with monthly contracts are more likely to churn",
                }
            )
        elif contract == "Two year":
            reasons.append(
                {
                    "factor": "Two-Year Contract",
                    "impact": "Low",
                    "detail": "Long-term contract reduces churn likelihood",
                }
            )
    if "MonthlyCharges" in customer_row.index and float(customer_row["MonthlyCharges"]) > 80:
        reasons.append(
            {
                "factor": "High Monthly Charges",
                "impact": "Medium",
                "detail": "Higher monthly bills correlate with increased churn",
            }
        )
    if "OnlineSecurity" in customer_row.index and str(customer_row["OnlineSecurity"]) == "No":
        reasons.append(
            {
                "factor": "No Online Security",
                "impact": "Medium",
                "detail": "Missing online security services increases churn risk",
            }
        )
    if "TechSupport" in customer_row.index and str(customer_row["TechSupport"]) == "No":
        reasons.append(
            {
                "factor": "No Tech Support",
                "impact": "Medium",
                "detail": "Lack of technical support access is a churn indicator",
            }
        )
    if not reasons:
        reasons.append(
            {
                "factor": "Stable Customer",
                "impact": "Low",
                "detail": "No significant churn indicators detected",
            }
        )
    return reasons
