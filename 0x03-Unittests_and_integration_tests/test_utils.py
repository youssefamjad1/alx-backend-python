#!/usr/bin/env python3
"""
Unit tests for access_nested_map from utils.py
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for access_nested_map function
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected output"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
