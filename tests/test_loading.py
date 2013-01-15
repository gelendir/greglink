import unittest

from greglink import loading
from mock import patch, mock_open, Mock

class TestRootPath(unittest.TestCase):

    @patch('greglink.loading.app')
    def test_root_path(self, app):
        app.config = {'TEST_ROOT': '/root'}

        expected = "/root"
        result = loading.root_path()

        self.assertEquals(result, expected)


class TestPathToFilePath(unittest.TestCase):

    @patch('greglink.loading.root_path')
    def test_path_to_filepath_with_beginning_slash(self, root_path):
        root_path.return_value = '/root'

        expected = "/root/foo/bar.md"
        result = loading.path_to_filepath("/foo/bar.md")

        self.assertEquals(result, expected)

    @patch('greglink.loading.root_path')
    def test_path_to_filepath_no_beginning_slash(self, root_path):
        root_path.return_value = '/root'

        expected = "/root/foo/bar.md"
        result = loading.path_to_filepath("foo/bar.md")

        self.assertEquals(result, expected)

    @patch('greglink.loading.root_path')
    def test_path_to_filepath_no_end_slash(self, root_path):
        root_path.return_value = '/root'

        expected = "/root/foo/bar/"
        result = loading.path_to_filepath("foo/bar/")

        self.assertEquals(result, expected)

class TestPathExists(unittest.TestCase):

    @patch('greglink.loading.root_path')
    @patch('greglink.loading.os.path.exists')
    def test_path_exists(self, os_exists, root_path):
        os_exists.return_value = False
        root_path.return_value = '/root'

        expected = False
        result = loading.path_exists("/foo.md")

        self.assertEquals(result, expected)
        os_exists.assert_called_once_with("/root/foo.md")

    @patch('greglink.loading.root_path')
    @patch('greglink.loading.os.path.exists')
    def test_path_exists(self, os_exists, root_path):
        os_exists.return_value = True
        root_path.return_value = '/root'

        expected = True
        result = loading.path_exists("/foo.md")

        self.assertEquals(result, expected)
        os_exists.assert_called_once_with("/root/foo.md")

class TestFindTest(unittest.TestCase):

    @patch('greglink.loading.path_to_filepath')
    @patch('greglink.loading.os.path.exists')
    def test_find_test_file_does_not_exist(self, os_exists, path_to_filepath):
        path = "/foo/bar.md"
        filepath = "/root/foo/bar.md"

        os_exists.return_value = False
        path_to_filepath.return_value = filepath

        expected = None
        result = loading.find_test(path)

        os_exists.assert_called_once_with(filepath)
        self.assertEquals(result, expected)

    @patch('greglink.loading.path_to_filepath')
    @patch('greglink.loading.os.path.exists')
    @patch('greglink.loading.load_test')
    def test_find_test(self, load_test, os_exists, path_to_filepath):
        path = "/foo/bar.md"
        filepath = "/root/foo/bar.md"

        testcase = Mock()
        load_test.return_value = testcase
        os_exists.return_value = True
        path_to_filepath.return_value = filepath

        result = loading.find_test(path)

        load_test.assert_called_once_with(path, filepath)
        self.assertEquals(result, testcase)

class TestLoadTest(unittest.TestCase):

    @patch('greglink.loading.load_testfile')
    def test_load_test_empty_file(self, load_testfile):
        load_testfile.return_value = (None, "")
        mockopen = mock_open()
        filepath = "/root/foo/bar.md"
        path = "/foo/bar.md"

        with patch('greglink.loading.open', mockopen, create=True):
            self.assertRaises(loading.NoHeaderInTestFile, loading.load_test,
                    path, filepath)

    @patch('greglink.loading.load_testfile')
    @patch('greglink.loading.TestCase')
    def test_load_test(self, TestCase, load_testfile):
        header = Mock()
        markup = Mock()
        path = "/foo/bar.md"
        filepath = "/root/foo/bar.md"
        load_testfile.return_value = (header, markup)

        mockopen = mock_open()
        with patch('greglink.loading.open', mockopen, create=True):
            testcase = loading.load_test(path, filepath)
            TestCase.assert_called_once_with(path, header, markup)


class TestAllTestFiles(unittest.TestCase):

    @patch('greglink.loading.os.path.exists')
    def test_all_testfiles_dir_does_not_exist(self, os_exists):
        os_exists.return_value = False

        expected = []
        result = loading.all_testfiles('/root')

        self.assertEquals(result, expected)

    @patch('greglink.loading.os.path.exists')
    @patch('greglink.loading.os.listdir')
    def test_all_testfiles_invalid_files(self, os_listdir, os_exists):
        os_exists.return_value = True
        os_listdir.return_value = ["foo"]

        expected = []
        result = list(loading.all_testfiles('/root'))

        os_listdir.assert_called_once_with
        self.assertEquals(result, expected)

    @patch('greglink.loading.os.path.exists')
    @patch('greglink.loading.os.listdir')
    def test_all_testfiles_one_valid_file(self, os_listdir, os_exists):
        os_exists.return_value = True
        os_listdir.return_value = ["foo", "bar.md"]

        expected = ["bar.md"]
        result = list(loading.all_testfiles('/root'))
        self.assertEquals(result, expected)

class TestAllTests(unittest.TestCase):

    @patch('greglink.loading.all_testfiles')
    @patch('greglink.loading.path_to_filepath')
    def test_all_tests_empty_folder(self, path_to_filepath, all_testfiles):
        path = "/"
        dirpath = "/root"
        path_to_filepath.return_value = dirpath
        all_testfiles.return_value = (f for f in [])

        expected = []
        result = loading.all_tests(path)

        self.assertEquals(result, expected)
        all_testfiles.assert_called_once_with(dirpath)

    @patch('greglink.loading.all_testfiles')
    @patch('greglink.loading.path_to_filepath')
    @patch('greglink.loading.load_test')
    def test_all_tests(self, load_test, path_to_filepath, all_testfiles):
        path = "/"
        dirpath = "/root"
        filepath = "/root/foo.md"
        urlpath = "/foo.md"
        filename = "foo.md"
        path_to_filepath.return_value = dirpath
        all_testfiles.return_value = (f for f in [filename])

        testcase = Mock()
        load_test.return_value = testcase

        expected = [testcase]
        result = loading.all_tests(path)

        path_to_filepath.assert_called_once_with(path)
        load_test.assert_called_once_with(urlpath, filepath)
        self.assertEquals(result, expected)

    @patch('greglink.loading.all_testfiles')
    @patch('greglink.loading.path_to_filepath')
    @patch('greglink.loading.load_test')
    def test_all_tests_two_level_root(self, load_test, path_to_filepath, all_testfiles):
        path = "/two/levels"
        dirpath = "/root/two/levels"
        filepath = "/root/two/levels/foo.md"
        urlpath = "/two/levels/foo.md"
        filename = "foo.md"
        path_to_filepath.return_value = dirpath
        all_testfiles.return_value = (f for f in [filename])

        testcase = Mock()
        load_test.return_value = testcase

        expected = [testcase]
        result = loading.all_tests(path)

        path_to_filepath.assert_called_once_with(path)
        load_test.assert_called_once_with(urlpath, filepath)
        self.assertEquals(result, expected)

if __name__ == "__main__":
    unittest.main()

