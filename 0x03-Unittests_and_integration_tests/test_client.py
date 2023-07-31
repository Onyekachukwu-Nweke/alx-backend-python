#!/usr/bin/env python3
"""
contain tests for class/methods in client.py
"""
import requests
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
# from utils import get_json, access_nested_map, memoize
from client import GithubOrgClient
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    test class for client.py
    """

    @parameterized.expand([
        ('google'),
        ('abc')
        ])
    @patch('client.get_json')
    def test_org(self, org_name, get_json_mock):
        """
        tests the org method in client.GithubOrgClient
        """
        endpoint = 'https://api.github.com/orgs/{}'.format(org_name)
        test = GithubOrgClient(org_name)
        test.org()
        test.org()
        get_json_mock.assert_called_once_with(endpoint)

    # @patch('GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self):
        """
        test _public_repos_url method in client.GithubOrgClient
        """
        return_dict = {
                "url": "https://api.github.com/orgs/google",
                "repos_url": "https://api.github.com/orgs/google/repos"
                }
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            test = GithubOrgClient('google')
            mock.return_value = return_dict
            _public_repos_url = test._public_repos_url
            repos_url = "https://api.github.com/orgs/google/repos"
            self.assertEqual(_public_repos_url, repos_url)

    @patch('client.get_json')
    def test_public_repos(self, get_json_mock):
        """
        test client.GithubOrgClient.public_repos method
        """
        return_repo = [
                {'repos_url': 'https://google/repo', "name": "google_repo"},
                {'repos_url': 'https://alx/repo', "name": "alx-repo"}
                ]
        get_json_mock.return_value = return_repo

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:

            test = GithubOrgClient('test')
            # mock_public_repos_url.return_value = test._public_repos_url
            repo_list = test.public_repos()
            self.assertEqual(["google_repo", "alx-repo"], repo_list)
            mock_public_repos_url.assert_called_once()
            get_json_mock.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
        ])
    def test_has_license(self, repo, license, expected):
        """
        test for client.GithubOrgClient.has_license
        """
        test = GithubOrgClient('test')
        result = test.has_license(repo, license)
        self.assertEqual(result, expected)


@parameterized_class(
        (org_payload, repos_payload, expected_repos, apache2_repos),
        TEST_PAYLOAD
        )
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test
    """
    @classmethod
    def setUpClass():
        """
        mocks request.get
        """
        config = {'return_value.json.side_effect': [cls.org_payload,
                                                    cls.repos_payload,
                                                    cls.expected_repos,
                                                    cls.apache2_repos]}
        cls.get_patcher = patch('requests.get', **config)
        req_mock = cls.get_patcher.start()

    @classmethod
    def tearDownClass():
        """
        stops patch
        """
        cls.get_patcher.stop()
