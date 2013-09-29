import os
import shutil
import tempfile
import unittest

from greglink.lib import navigation
from mock import patch, Mock

SANDBOX_ROOT = "/tmp/greglink_tests"
ROOT_NAME = os.path.basename(SANDBOX_ROOT)

def mkdir(path):
    os.mkdir(path)

def mkfile(path, content=''):
    with open(path, 'w') as f:
        f.write(content)

def rmdir(path):
    shutil.rmtree(path)

def empty_dir(root):
    for path in os.listdir(root):
        fullpath = os.path.join(root, path)
        if os.path.isfile(fullpath):
            os.remove(fullpath)
        else:
            rmdir(fullpath)

class TestGenerateTree(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = SANDBOX_ROOT
        mkdir(cls.root)

    @classmethod
    def tearDownClass(cls):
        rmdir(cls.root)

    def setUp(self):
        empty_dir(self.root)

    def test_empty_directory(self):
        expected = []

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)

    @patch('greglink.lib.navigation.url_for', Mock(return_value='/foo'))
    def test_one_file(self):
        mkfile(os.path.join(self.root, 'foo'))

        expected = [
            {'title': 'foo', 'href': '/foo', 'key': '/foo'}
        ]

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)

    @patch('greglink.lib.navigation.url_for')
    def test_two_files(self, url_for):
        mkfile(os.path.join(self.root, 'foo'))
        mkfile(os.path.join(self.root, 'bar'))

        url_for.side_effect = ['/bar', '/foo']

        expected = [
            {'title': 'bar', 'href': '/bar', 'key': '/bar'},
            {'title': 'foo', 'href': '/foo', 'key': '/foo'},
        ]

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)

    def test_one_dir(self):
        mkdir(os.path.join(self.root, 'foo'))

        expected = [
            {'title': 'foo', 'isFolder': True, 'children': []}
        ]

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)

    @patch('greglink.lib.navigation.url_for')
    def test_one_dir_one_file(self, url_for):
        mkdir(os.path.join(self.root, 'foo'))
        mkfile(os.path.join(self.root, 'bar'))

        url_for.return_value = '/bar'

        expected = [
            {'title': 'foo', 'isFolder': True, 'children': []},
            {'title': 'bar', 'href': '/bar', 'key': '/bar'},
        ]

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)


    @patch('greglink.lib.navigation.url_for')
    def test_one_file_one_dir_one_file(self, url_for):
        mkfile(os.path.join(self.root, 'bar'))
        mkdir(os.path.join(self.root, 'foo'))
        mkfile(os.path.join(self.root, 'foo', 'spam'))

        def url_mock(route, path):
            return path
        url_for.side_effect = url_mock

        expected = [
            {'title': 'foo', 'isFolder': True, 'children': [
                {'title': 'spam', 'href': '/foo/spam', 'key': '/foo/spam'}
            ]},
            {'title': 'bar', 'href': '/bar', 'key': '/bar'}
        ]

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)

    @patch('greglink.lib.navigation.url_for')
    def test_two_nested_dirs_one_file(self, url_for):
        mkdir(os.path.join(self.root, 'foo'))
        mkdir(os.path.join(self.root, 'foo', 'bar'))
        mkfile(os.path.join(self.root, 'foo', 'bar', 'spam'))

        url_for.return_value = '/foo/bar/spam'

        expected = [
            {'title': 'foo', 'isFolder': True, 'children': [
                {'title': 'bar', 'isFolder': True, 'children': [
                    {'title': 'spam',
                     'href': '/foo/bar/spam',
                     'key': '/foo/bar/spam'}
                ]}
            ]}
        ]

        result = navigation.generate_tree(self.root)

        self.assertEquals(result, expected)

if __name__ == "__main__":
    unittest.main()
