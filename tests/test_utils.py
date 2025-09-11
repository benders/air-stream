"""
Tests for utils.py module
"""

import unittest
import sys
import os

# Add the lib directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))

from utils import format_time

class TestFormatTime(unittest.TestCase):
    """Tests for the format_time function"""
    
    def test_format_time_8_tuple(self):
        """Test format_time with an 8-tuple (standard format)"""
        # (year, month, mday, hour, minute, second, weekday, yearday)
        time_tuple = (2025, 9, 11, 14, 30, 45, 3, 254)
        result = format_time(time_tuple)
        expected = "2025-09-11 14:30:45"
        self.assertEqual(result, expected)
    
    def test_format_time_9_tuple(self):
        """Test format_time with a 9-tuple (includes isdst)"""
        # (year, month, mday, hour, minute, second, weekday, yearday, isdst)
        time_tuple = (2025, 9, 11, 14, 30, 45, 3, 254, 1)
        result = format_time(time_tuple)
        expected = "2025-09-11 14:30:45"
        self.assertEqual(result, expected)
    
    def test_format_time_padding(self):
        """Test format_time pads single-digit values correctly"""
        time_tuple = (2025, 1, 2, 3, 4, 5, 3, 2)
        result = format_time(time_tuple)
        expected = "2025-01-02 03:04:05"
        self.assertEqual(result, expected)
    
    def test_format_time_empty_tuple(self):
        """Test format_time with an empty tuple (should raise an error)"""
        with self.assertRaises(ValueError):
            format_time(())
    
    def test_format_time_partial_tuple(self):
        """Test format_time with a partial tuple (should raise an error)"""
        with self.assertRaises(ValueError):
            format_time((2025, 9, 11))