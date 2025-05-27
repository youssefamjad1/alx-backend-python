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

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that access_nested_map raises KeyError with the missing key"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], expected_key)

if __name__ == "__main__":
    unittest.main()

