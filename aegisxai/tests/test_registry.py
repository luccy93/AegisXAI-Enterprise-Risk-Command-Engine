"""Registry validation — test PAGE_FUNCTIONS dict merge for conflicts."""
import pytest


def test_app_page_functions_merge():
    """Verify that the merged PAGE_FUNCTIONS in app.py has no duplicate keys."""
    import ast, sys
    with open("app.py") as f:
        tree = ast.parse(f.read())

    # Find the PAGE_FUNCTIONS dict assignment
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "PAGE_FUNCTIONS":
                    if isinstance(node.value, ast.Dict):
                        keys = [k.value if isinstance(k, ast.Str) else k.s for k in node.value.keys if k is not None]
                        seen = set()
                        for k in keys:
                            assert k not in seen, f"Duplicate key in merged PAGE_FUNCTIONS: '{k}'"
                            seen.add(k)
                        return
    pytest.fail("Could not find PAGE_FUNCTIONS dict assignment in app.py")


def test_nav_items_no_duplicates():
    """Verify no duplicate keys in NAV_ITEMS."""
    import ast
    with open("app.py") as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "NAV_ITEMS":
                    if isinstance(node.value, ast.List):
                        keys = []
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Tuple) and len(elt.elts) > 1:
                                key_elt = elt.elts[1]
                                if isinstance(key_elt, ast.Constant) and key_elt.value is not None:
                                    keys.append(key_elt.value)
                        seen = set()
                        for k in keys:
                            assert k not in seen, f"Duplicate nav key: '{k}'"
                            seen.add(k)
                        return
    pytest.fail("Could not find NAV_ITEMS list in app.py")


def test_service_modules_importable():
    """Verify all service modules can be imported."""
    modules = [
        "aegisxai.services.prediction_service",
        "aegisxai.services.xai_service",
        "aegisxai.services.alert_service",
        "aegisxai.services.clv_service",
        "aegisxai.services.anomaly_service",
        "aegisxai.services.compliance_service",
        "aegisxai.services.copilot_service",
        "aegisxai.services.forecasting_service",
        "aegisxai.services.retention_agent",
        "aegisxai.services.integration_service",
        "aegisxai.services.pipeline_service",
        "aegisxai.services.recommendation_service",
        "aegisxai.services.advanced_features",
        "aegisxai.services.premium_services",
        "aegisxai.services.premium_ux",
    ]
    for mod_name in modules:
        __import__(mod_name)


def test_utility_modules_importable():
    modules = [
        "aegisxai.utils.helpers",
        "aegisxai.utils.logging",
        "aegisxai.utils.caching",
        "aegisxai.utils.data_profiler",
        "aegisxai.utils.export",
        "aegisxai.utils.bootstrap",
    ]
    for mod_name in modules:
        __import__(mod_name)


def test_auth_module_importable():
    from aegisxai.auth.auth import authenticate, hash_password, verify_password
    assert callable(authenticate)
    assert callable(hash_password)
    assert callable(verify_password)


def test_config_settings_importable():
    from aegisxai.config.settings import Settings
    assert hasattr(Settings, "CSV_PATH")


def test_model_modules_importable():
    from aegisxai.models.features import load_data, engineer_features
    from aegisxai.models.registry import init_registry
    assert callable(load_data)
    assert callable(engineer_features)
    assert callable(init_registry)
