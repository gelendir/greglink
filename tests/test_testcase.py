import unittest

from greglink.models.testcase import TestCase
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

    def test_testcase_path(self):
        path = "/foo/bar.md"
        testcase = TestCase(path, Mock(), Mock())

        self.assertEquals(testcase.path, '/foo/bar.md')

    @patch("greglink.models.testcase.convert_markup")
    def test_testcase_to_html(self, convert_markup):
        markup = Mock()
        testcase = TestCase(Mock(), Mock(), markup)

        expected = "<h1>hello world</h1>"
        convert_markup.return_value = expected

        result = testcase.to_html()
        convert_markup.assert_called_once_with(markup)
        self.assertEquals(result, expected)


if __name__ == "__main__":
    unittest.main()
