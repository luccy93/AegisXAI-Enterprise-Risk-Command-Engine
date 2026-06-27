"""Tests for utility modules."""
import pytest
import pandas as pd
import numpy as np


class TestDataProfiler:
    def test_profile_dataframe(self, sample_df):
        from aegisxai.utils.data_profiler import profile_dataframe
        profile = profile_dataframe(sample_df, name="Test")
        assert profile["name"] == "Test"
        assert profile["rows"] == len(sample_df)
        assert profile["columns"] == len(sample_df.columns)
        assert "column_profiles" in profile
        for col in sample_df.columns:
            assert col in profile["column_profiles"]

    def test_validate_churn_data_valid(self, sample_df):
        from aegisxai.utils.data_profiler import validate_churn_data
        result = validate_churn_data(sample_df)
        assert "valid" in result
        assert "issues" in result
        assert "score" in result

    def test_validate_churn_data_missing_cols(self):
        from aegisxai.utils.data_profiler import validate_churn_data
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = validate_churn_data(df)
        assert result["valid"] is False
        assert len(result["issues"]) > 0

    def test_segment_summary(self, sample_df):
        from aegisxai.utils.data_profiler import segment_summary
        summary = segment_summary(sample_df, "Contract", "MonthlyCharges")
        assert isinstance(summary, list)

    def test_correlation_report(self, sample_df):
        from aegisxai.utils.data_profiler import correlation_report
        report = correlation_report(sample_df)
        assert "matrix" in report
        assert "top_pairs" in report


class TestExport:
    def test_to_csv_string(self, sample_df):
        from aegisxai.utils.export import to_csv_string
        csv_str = to_csv_string(sample_df)
        assert isinstance(csv_str, str)
        assert "customerID" in csv_str

    def test_to_json_string(self, sample_df):
        from aegisxai.utils.export import to_json_string
        json_str = to_json_string(sample_df)
        assert isinstance(json_str, str)

    def test_to_html_table(self, sample_df):
        from aegisxai.utils.export import to_html_table
        html = to_html_table(sample_df)
        assert "<html>" in html
        assert "dataframe" in html

    def test_export_churn_summary(self, sample_df):
        from aegisxai.utils.export import export_churn_summary
        summary = export_churn_summary(sample_df)
        assert "summary" in summary
        assert "churn_rate" in summary["summary"]

    def test_export_to_markdown(self, sample_df):
        from aegisxai.utils.data_profiler import profile_dataframe
        from aegisxai.utils.export import export_to_markdown
        profile = profile_dataframe(sample_df)
        md = export_to_markdown(profile)
        assert isinstance(md, str)
        assert "# Data Profile" in md
