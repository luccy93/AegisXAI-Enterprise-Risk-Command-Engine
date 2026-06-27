"""Export utilities for reports, data, and visualizations."""
import io
import csv
import json
import pandas as pd


def to_csv_string(df):
    """Convert DataFrame to CSV string."""
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()


def to_json_string(data, orient="records"):
    """Convert data to JSON string."""
    if isinstance(data, pd.DataFrame):
        return data.to_json(orient=orient, indent=2)
    return json.dumps(data, indent=2, default=str)


def to_html_table(df, title="Report", max_rows=200):
    """Convert DataFrame to an HTML table with basic styling."""
    html = df.head(max_rows).to_html(index=False, classes="dataframe", border=0)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          padding: 20px; background: #0f172a; color: #e2e8f0; }}
  h1 {{ color: #38bdf8; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
  th {{ background: #1e293b; color: #94a3b8; padding: 8px 12px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #1e293b; font-size: 13px; }}
  tr:hover td {{ background: #1e293b40; }}
  .meta {{ color: #64748b; font-size: 12px; margin-bottom: 8px; }}
</style></head><body>
<h1>{title}</h1>
<div class="meta">{len(df)} rows &middot; {len(df.columns)} columns</div>
{html}
</body></html>"""


def export_churn_summary(df):
    """Generate a structured churn summary suitable for JSON export."""
    total = len(df)
    churned = int((df["Churn"] == "Yes").sum())
    retained = total - churned
    return {
        "summary": {
            "total_customers": total,
            "churned": churned,
            "retained": retained,
            "churn_rate": round(churned / total, 4) if total else 0,
        },
        "by_contract": df.groupby("Contract")["Churn"].apply(
            lambda x: {"total": int(len(x)), "churned": int((x == "Yes").sum())}
        ).to_dict(),
        "by_internet": df.groupby("InternetService")["Churn"].apply(
            lambda x: {"total": int(len(x)), "churned": int((x == "Yes").sum())}
        ).to_dict(),
        "avg_metrics": {
            "tenure": round(df["tenure"].mean(), 1),
            "monthly_charges": round(df["MonthlyCharges"].mean(), 2),
            "total_charges": round(df["TotalCharges"].mean(), 2),
        },
    }


def export_to_markdown(profile):
    """Convert a data profile dict to markdown summary."""
    lines = [f"# Data Profile: {profile['name']}", ""]
    lines.append(f"- **Rows:** {profile['rows']:,}")
    lines.append(f"- **Columns:** {profile['columns']}")
    lines.append(f"- **Memory:** {profile['memory_mb']} MB")
    lines.append(f"- **Duplicates:** {profile['duplicate_rows']:,}")
    lines.append(f"- **Missing cells:** {profile['missing_cells']:,} ({profile['missing_pct']}%)")
    lines.append("")
    lines.append("## Column Details")
    lines.append("")
    lines.append("| Column | Type | Missing% | Unique | Range / Top Values |")
    lines.append("|--------|------|----------|--------|-------------------|")
    for col, cp in profile["column_profiles"].items():
        if "mean" in cp:
            extra = f"{cp['min']} ~ {cp['max']} (mean={cp['mean']})"
        elif "top_values" in cp:
            extra = ", ".join(f"{k}({v})" for k, v in list(cp["top_values"].items())[:3])
        else:
            extra = "-"
        lines.append(f"| {col} | {cp['dtype']} | {cp['missing_pct']}% | {cp['unique']} | {extra} |")
    return "\n".join(lines)
