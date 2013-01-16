import os
import shutil
import tempfile
import unittest

from greglink.lib import jstree
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
        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)

    def test_one_file(self):
        mkfile(os.path.join(self.root, 'foo'))

        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [{
                'data': 'foo',
                'attr': {'href': '/foo'},
            }],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)

    def test_two_files(self):
        mkfile(os.path.join(self.root, 'foo'))
        mkfile(os.path.join(self.root, 'bar'))

        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [
                {
                    'data': 'bar',
                    'attr': {'href': '/bar'},
                },
                {
                    'data': 'foo',
                    'attr': {'href': '/foo'},
                },
            ],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)

    def test_one_dir(self):
        mkdir(os.path.join(self.root, 'foo'))

        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [{
                'data': 'foo',
                'attr': {'href': '/foo'},
                'children': [],
            }],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)

    def test_one_dir_one_file(self):
        mkdir(os.path.join(self.root, 'foo'))
        mkfile(os.path.join(self.root, 'bar'))

        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [
                {
                'data': 'bar',
                'attr': {'href': '/bar'},
                },
                {
                'data': 'foo',
                'attr': {'href': '/foo'},
                'children': [],
                }
            ],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)


    def test_one_file_one_dir_one_file(self):
        mkfile(os.path.join(self.root, 'bar'))
        mkdir(os.path.join(self.root, 'foo'))
        mkfile(os.path.join(self.root, 'foo', 'spam'))

        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [
                {
                    'data': 'bar',
                    'attr': {'href': '/bar'},
                },
                {
                    'data': 'foo',
                    'attr': {'href': '/foo'},
                    'children': [
                        {
                        'data': 'spam',
                        'attr': {'href': '/foo/spam'},
                        },
                    ]
                }
            ],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)

    def test_two_nested_dirs_one_file(self):
        mkdir(os.path.join(self.root, 'foo'))
        mkdir(os.path.join(self.root, 'foo', 'bar'))
        mkfile(os.path.join(self.root, 'foo', 'bar', 'spam'))

        expected = {
            'data': ROOT_NAME,
            'attr': {'href': '/'},
            'children': [
                {
                    'data': 'foo',
                    'attr': {'href': '/foo'},
                    'children': [
                        {
                            'data': 'bar',
                            'attr': {'href': '/foo/bar'},
                            'children': [
                                {
                                    'data': 'spam',
                                    'attr': {'href': '/foo/bar/spam'},
                                }
                            ],
                        },
                    ]
                }
            ],
        }

        result = jstree.generate_tree(self.root)

        self.assertEquals(result, expected)

if __name__ == "__main__":
    unittest.main()
