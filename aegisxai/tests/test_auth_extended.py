"""Extended authentication tests."""
import pytest


class TestAuth:
    def test_hash_password(self):
        from aegisxai.auth.auth import hash_password
        h = hash_password("hello123")
        assert h != "hello123"
        assert len(h) == 64  # SHA-256 hex digest

    def test_verify_password_correct(self):
        from aegisxai.auth.auth import hash_password, verify_password
        h = hash_password("test_pass")
        assert verify_password("test_pass", h) is True

    def test_verify_password_wrong(self):
        from aegisxai.auth.auth import hash_password, verify_password
        h = hash_password("test_pass")
        assert verify_password("wrong_pass", h) is False

    def test_authenticate_admin(self):
        from aegisxai.auth.auth import authenticate
        user = authenticate("admin", "admin123")
        assert user is not None
        assert user["role"] == "Admin"

    def test_authenticate_invalid(self):
        from aegisxai.auth.auth import authenticate
        user = authenticate("admin", "wrongpassword")
        assert user is None

    def test_authenticate_unknown_user(self):
        from aegisxai.auth.auth import authenticate
        user = authenticate("unknown", "password")
        assert user is None

    def test_authorized_pages_admin(self):
        from aegisxai.auth.auth import get_authorized_pages
        pages = get_authorized_pages("Admin")
        assert len(pages) > 0

    def test_authorized_pages_viewer(self):
        from aegisxai.auth.auth import get_authorized_pages
        pages = get_authorized_pages("Viewer")
        assert len(pages) > 0
