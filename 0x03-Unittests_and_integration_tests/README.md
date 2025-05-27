# 0x03. Unittests and Integration Tests

This directory contains Python unit tests and integration tests for backend development, part of the **ALX Backend Python** module.

## 📚 Learning Objectives

By completing these tasks, you will learn:

- The difference between unit tests and integration tests.
- How to write unit tests in Python using `unittest`.
- How to use testing tools like `@parameterized.expand`, `mock`, and `fixtures`.
- Best practices for testing in a backend environment.

## 📁 Files

- `utils.py`: Contains utility functions such as `access_nested_map`, `get_json`, and `memoize`.
- `test_utils.py`: Unit tests for functions in `utils.py`, including parameterized test cases.
- `client.py`, `fixtures.py`: Will be used in future tasks (not required for Task 0).

## ✅ How to Run Tests

Use the following command:

```bash
python -m unittest test_utils.py

