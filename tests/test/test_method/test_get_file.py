"""Telemulator API GetFile method.

make test T=test_method/test_get_file.py
"""
from . import TestMethod


class TestGetFile(TestMethod):
    """Test for GetFile method."""

    def test_dflt(self):
        """Test method call."""
        # print('###')
        # self.telemul.print_trace(True)
        answer = self.bot.get_file('wwwxxxyyy')
        assert answer.file_size == 500
