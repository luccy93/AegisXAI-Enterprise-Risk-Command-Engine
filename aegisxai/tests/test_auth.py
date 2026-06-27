import pytest
import hashlib
from aegisxai.auth.auth import authenticate, get_role_permissions, check_page_access

def test_authenticate_valid():
    result = authenticate("admin", "admin123", "Admin")
    assert result is not None
    assert result["username"] == "admin"
    assert result["role"] == "Admin"

def test_authenticate_invalid_password():
    result = authenticate("admin", "wrong", "Admin")
    assert result is None

def test_authenticate_invalid_user():
    result = authenticate("nobody", "pass", "Viewer")
    assert result is None

def test_get_role_permissions_admin():
    perms = get_role_permissions("Admin")
    assert "admin" in perms

def test_get_role_permissions_viewer():
    perms = get_role_permissions("Viewer")
    assert "view" in perms

def test_check_page_access_admin():
    assert check_page_access("Dashboard", "Admin") == True

def test_check_page_access_restricted():
    result = check_page_access("Settings", "Viewer")
    assert result == False
