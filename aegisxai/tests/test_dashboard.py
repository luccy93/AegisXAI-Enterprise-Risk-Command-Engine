import pytest
import streamlit as st

def test_session_state_defaults():
    assert hasattr(st, "session_state")

def test_nav_items_not_empty():
    from aegisxai.app import NAV_ITEMS
    assert len(NAV_ITEMS) >= 10

def test_page_functions_not_empty():
    from aegisxai.app import PAGE_FUNCTIONS
    assert len(PAGE_FUNCTIONS) >= 25

def test_themes_defined():
    from aegisxai.app import THEMES
    assert len(THEMES) >= 5
    assert "Quantum Aurora" in THEMES
