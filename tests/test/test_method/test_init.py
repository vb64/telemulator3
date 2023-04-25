"""Telemulator API methods support functions.

make test T=test_method/test_init.py
"""
from . import TestMethod


class TestInit(TestMethod):
    """Test __init__.py module."""

    def test_error(self):
        """Check error function."""
        from telemulator3.method import error

        code, data = error(100, 'xxx')
        assert code == 100
        assert data['ok'] is False
        assert data['error_code'] == 100
        assert data['description'] == 'xxx'
