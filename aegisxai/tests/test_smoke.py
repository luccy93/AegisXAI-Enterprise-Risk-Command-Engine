"""Smoke tests — verify all page functions are importable and callable."""
import pytest


def test_page_registry_no_duplicates():
    from aegisxai.dashboards.pages import PAGE_FUNCTIONS as CORE
    from aegisxai.dashboards.cx_pages import CX_PAGE_FUNCTIONS
    from aegisxai.dashboards.enterprise_pages import ENTERPRISE_PAGE_FUNCTIONS
    from aegisxai.dashboards.ai_pages import AI_PAGE_FUNCTIONS
    from aegisxai.dashboards.ops_pages import OPS_PAGE_FUNCTIONS
    from aegisxai.dashboards.biz_pages import BIZ_PAGE_FUNCTIONS
    from aegisxai.dashboards.corp_pages import CORP_PAGE_FUNCTIONS
    from aegisxai.dashboards.premium_dashboards import PREMIUM_PAGE_FUNCTIONS
    from aegisxai.dashboards.ux_pages import UX_PAGE_FUNCTIONS

    all_keys = {}
    for name, module in [
        ("core", CORE), ("cx", CX_PAGE_FUNCTIONS),
        ("enterprise", ENTERPRISE_PAGE_FUNCTIONS),
        ("ai", AI_PAGE_FUNCTIONS), ("ops", OPS_PAGE_FUNCTIONS),
        ("biz", BIZ_PAGE_FUNCTIONS), ("corp", CORP_PAGE_FUNCTIONS),
        ("premium", PREMIUM_PAGE_FUNCTIONS), ("ux", UX_PAGE_FUNCTIONS),
    ]:
        for key in module:
            if key in all_keys:
                pytest.fail(f"Duplicate key '{key}' in {name} (also in {all_keys[key]})")
            all_keys[key] = name

    assert len(all_keys) >= 80, f"Expected 80+ pages, got {len(all_keys)}"


def test_all_core_pages_importable():
    from aegisxai.dashboards.pages import PAGE_FUNCTIONS
    for name, func in PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_cx_pages_importable():
    from aegisxai.dashboards.cx_pages import CX_PAGE_FUNCTIONS
    for name, func in CX_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_enterprise_pages_importable():
    from aegisxai.dashboards.enterprise_pages import ENTERPRISE_PAGE_FUNCTIONS
    for name, func in ENTERPRISE_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_ai_pages_importable():
    from aegisxai.dashboards.ai_pages import AI_PAGE_FUNCTIONS
    for name, func in AI_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_ops_pages_importable():
    from aegisxai.dashboards.ops_pages import OPS_PAGE_FUNCTIONS
    for name, func in OPS_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_biz_pages_importable():
    from aegisxai.dashboards.biz_pages import BIZ_PAGE_FUNCTIONS
    for name, func in BIZ_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_corp_pages_importable():
    from aegisxai.dashboards.corp_pages import CORP_PAGE_FUNCTIONS
    for name, func in CORP_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_premium_pages_importable():
    from aegisxai.dashboards.premium_dashboards import PREMIUM_PAGE_FUNCTIONS
    for name, func in PREMIUM_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_all_ux_pages_importable():
    from aegisxai.dashboards.ux_pages import UX_PAGE_FUNCTIONS
    for name, func in UX_PAGE_FUNCTIONS.items():
        assert callable(func), f"{name} is not callable"


def test_app_compiles():
    import ast
    with open("app.py") as f:
        ast.parse(f.read())


def test_aegisxai_app_compiles():
    import ast
    with open("aegisxai/app.py") as f:
        ast.parse(f.read())
