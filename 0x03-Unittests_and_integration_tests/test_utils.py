#!/usr/bin/env python3
"""
contains tests for utils.py
"""
import utils
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """
    test class for access_nested_map in utils.py
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, paramA, paramB, out):
        """tests the function in utils.py"""
        self.assertEqual(access_nested_map(paramA, paramB), out)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, paramA, paramB):
        """test for if an exception is raised"""
        with self.assertRaises(KeyError):
            access_nested_map(paramA, paramB)


class TestGetJson(unittest.TestCase):
    """
    test class of get_json in utils.py
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, url, expected):
        """
        tests external http calls
        """

        with patch('utils.requests') as mock_requests:
            response = Mock()
            mock_requests.get.return_value = response
            response.json.return_value = expected
            self.assertEqual(get_json(url), response.json.return_value)


class TestMemoize(unittest.TestCase):
    """
    tests the memoize decorator in utils.py
    """

    def test_memoize(self):
        """
        test for memoize decorator
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass, 'a_method') as mocked:
            test = TestClass()
            test.a_property()
            test.a_property()
            mocked.assert_called_once()
            mocked.return_value = 42
            self.assertEqual(mocked(), 42)
