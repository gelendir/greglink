import unittest

from greglink.models.testcase import TestCase, NoHeaderInTestfile, load_file
from mock import patch, Mock, mock_open

class TestTestCase(unittest.TestCase):

    def test_testcase_id(self):
        header = {'title': 'foo', 'id': 'bar'}
        testcase = TestCase(Mock(), header, Mock())

        self.assertEquals(testcase.id, 'bar')

    def test_testcase_title(self):
        header = {'title': 'foo', 'id': 'bar'}
        testcase = TestCase(Mock(), header, Mock())

        self.assertEquals(testcase.title, 'foo')

    def test_testcase_filename(self):
        filepath = "/foo/bar.md"
        testcase = TestCase(filepath, Mock(), Mock())

        self.assertEquals(testcase.filename, 'bar.md')

    @patch("greglink.models.testcase.convert_markup")
    def test_testcase_to_html(self, convert_markup):
        markup = Mock()
        testcase = TestCase(Mock(), Mock(), markup)

        expected = "<h1>hello world</h1>"
        convert_markup.return_value = expected

        result = testcase.to_html()
        convert_markup.assert_called_once_with(markup)
        self.assertEquals(result, expected)

class TestLoadFile(unittest.TestCase):

    @patch('greglink.models.testcase.load_testfile')
    def test_load_file_empty_file(self, load_testfile):
        load_testfile.return_value = (None, "")
        mockopen = mock_open()

        with patch('greglink.models.testcase.open', mockopen, create=True):
            self.assertRaises(NoHeaderInTestfile, load_file, "foobar")

    @patch('greglink.models.testcase.load_testfile')
    def test_load_file(self, load_testfile):
        header = Mock()
        markup = Mock()
        filepath = "foobar"
        load_testfile.return_value = (header, markup)

        mockopen = mock_open()
        with patch('greglink.models.testcase.open', mockopen, create=True):
            testcase = load_file(filepath)
            self.assertEquals(testcase.filepath, filepath)
            self.assertEquals(testcase.header, header)
            self.assertEquals(testcase.markup, markup)


if __name__ == "__main__":
    unittest.main()
