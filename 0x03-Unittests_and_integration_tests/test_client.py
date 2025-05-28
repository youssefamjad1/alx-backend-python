#!/usr/bin/env python3
"""
Test cases for GithubOrgClient class
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result"""
        mock_get_json.return_value = {"mocked": True}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"mocked": True})

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        client = GithubOrgClient("test_org")
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=unittest.mock.PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://some.url/repo"}
            self.assertEqual(
                client._public_repos_url,
                "http://some.url/repo"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        client = GithubOrgClient("test_org")
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=unittest.mock.PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://some.url"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license with different licenses"""
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client.has_license(repo, license_key),
            expected
        )


class MockResponse:
    """Mock response class for requests.get to simulate HTTP responses"""
    
    def __init__(self, json_data):
        """Initialize MockResponse with JSON data to be returned"""
        self._json_data = json_data

    def json(self):
        """Return the JSON data that was provided during initialization"""
        return self._json_data


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to start patcher"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method in integration test"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filtering"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
