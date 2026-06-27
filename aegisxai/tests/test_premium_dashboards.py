"""Tests for premium dashboard data services."""
import pytest
import pandas as pd


class TestExecutiveKPI:
    def test_get_exec_kpi_sparklines(self):
        from aegisxai.services.premium_services import get_exec_kpi_sparklines
        kpis = get_exec_kpi_sparklines()
        assert isinstance(kpis, dict)
        for key in ("revenue", "churn", "customers", "clv"):
            assert key in kpis
            assert "value" in kpis[key] and "delta" in kpis[key]

    def test_get_revenue_breakdown(self):
        from aegisxai.services.premium_services import get_revenue_breakdown
        rev = get_revenue_breakdown()
        assert isinstance(rev, pd.DataFrame)
        assert not rev.empty


class TestScenarioSimulation:
    def test_get_scenario_defaults(self):
        from aegisxai.services.premium_services import get_scenario_defaults
        defaults = get_scenario_defaults()
        assert isinstance(defaults, dict)
        for key in ("contract_mix", "monthly_charges", "tenure"):
            assert key in defaults

    def test_run_scenario(self):
        from aegisxai.services.premium_services import run_scenario
        result = run_scenario({})
        assert isinstance(result, dict)
        assert "churn_rate" in result or "predicted_churn" in result


class TestSHAPService:
    def test_get_shap_waterfall(self):
        from aegisxai.services.premium_services import get_shap_waterfall
        data = get_shap_waterfall()
        assert isinstance(data, list) or isinstance(data, dict)

    def test_get_shap_summary(self):
        from aegisxai.services.premium_services import get_shap_summary
        summary = get_shap_summary()
        assert isinstance(summary, list) or "features" in str(type(summary))


class TestSecurityGovernance:
    def test_get_compliance_status(self):
        from aegisxai.services.premium_services import get_compliance_status
        status = get_compliance_status()
        assert isinstance(status, dict)
        assert "gdpr" in status or "soc2" in status


class TestReporting:
    def test_generate_report(self):
        from aegisxai.services.premium_services import generate_report
        report = generate_report("executive_summary")
        assert isinstance(report, dict) or isinstance(report, str)

    def test_get_report_templates(self):
        from aegisxai.services.premium_services import get_report_templates
        templates = get_report_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0


class TestWidgets:
    def test_get_world_clocks(self):
        from aegisxai.services.premium_ux import get_world_clocks
        clocks = get_world_clocks()
        assert isinstance(clocks, list)
        assert len(clocks) >= 3

    def test_get_calendar_events(self):
        from aegisxai.services.premium_ux import get_calendar_events
        events = get_calendar_events()
        assert isinstance(events, list)
        for ev in events:
            assert "title" in ev and "date" in ev

    def test_get_mini_metrics(self):
        from aegisxai.services.premium_ux import get_mini_metrics
        metrics = get_mini_metrics()
        for key in ("cpu", "memory", "sessions"):
            assert key in metrics

    def test_get_achievements(self):
        from aegisxai.services.premium_ux import get_achievements
        ach = get_achievements()
        assert "top_agent" in ach
        assert "leaderboard" in ach or "badges" in ach

    def test_get_search_results(self):
        from aegisxai.services.premium_ux import get_search_results
        results = get_search_results("C1001")
        assert isinstance(results, list)
        assert len(results) > 0
