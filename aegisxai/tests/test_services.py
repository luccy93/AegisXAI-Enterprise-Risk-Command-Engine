"""Tests for service modules."""
import pytest
import pandas as pd
import numpy as np


class TestPremiumUX:
    def test_get_boot_sequence(self):
        from aegisxai.services.premium_ux import get_boot_sequence
        items = get_boot_sequence()
        assert len(items) == 6
        for item in items:
            assert "label" in item
            assert "status" in item
            assert item["status"] in ("done", "active", "pending")

    def test_get_notifications(self):
        from aegisxai.services.premium_ux import get_notifications
        notifs = get_notifications()
        assert isinstance(notifs, dict)
        assert len(notifs) >= 1
        for cat, items in notifs.items():
            assert isinstance(items, list)
            for item in items:
                assert "title" in item
                assert "color" in item

    def test_get_activities(self):
        from aegisxai.services.premium_ux import get_activities
        acts = get_activities(5)
        assert len(acts) == 5
        for a in acts:
            assert "icon" in a and "text" in a and "time" in a

    def test_get_system_status(self):
        from aegisxai.services.premium_ux import get_system_status
        s = get_system_status()
        for key in ("cpu", "memory", "sessions", "health", "database"):
            assert key in s

    def test_get_model_health_status(self):
        from aegisxai.services.premium_ux import get_model_health_status
        h = get_model_health_status()
        assert "accuracy" in h and "drift" in h
        assert 0 < h["accuracy"] < 1
        assert 0 < h["drift"] < 1


class TestPremiumServices:
    def test_get_alerts_returns_dataframe(self):
        from aegisxai.services.premium_services import get_alerts
        df = get_alerts()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert all(c in df.columns for c in ("id", "severity", "title", "status"))

    def test_get_live_events(self):
        from aegisxai.services.premium_services import get_live_events
        df = get_live_events(10)
        assert len(df) == 10

    def test_get_model_metrics(self):
        from aegisxai.services.premium_services import get_model_metrics
        m = get_model_metrics()
        assert "roc_auc" in m

    def test_get_scenario_defaults(self):
        from aegisxai.services.premium_services import get_scenario_defaults
        s = get_scenario_defaults()
        assert "contract_mix" in s


class TestCopilotService:
    def test_process_query_known(self):
        from aegisxai.services.copilot_service import process_query
        result = process_query("Show critical customers", "admin")
        assert result is not None

    def test_process_query_unknown(self):
        from aegisxai.services.copilot_service import process_query
        result = process_query("xyz not a real query", "admin")
        assert result is not None


class TestForecastingService:
    def test_get_forecast(self):
        from aegisxai.services.forecasting_service import get_forecast
        periods = 12
        forecast = get_forecast(periods=periods)
        assert len(forecast) == periods
        for row in forecast:
            assert "ds" in row and "yhat" in row


class TestPredictionService:
    def test_predict_single(self, sample_customer):
        from aegisxai.services.prediction_service import predict_single
        result = predict_single(sample_customer)
        assert "prediction" in result
        assert "probability" in result
        assert result["prediction"] in (0, 1)
        assert 0 <= result["probability"] <= 1


class TestFeatures:
    def test_load_data(self):
        from aegisxai.models.features import load_data
        df = load_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_engineer_features(self, sample_df):
        from aegisxai.models.features import engineer_features
        df = engineer_features(sample_df)
        assert isinstance(df, pd.DataFrame)
