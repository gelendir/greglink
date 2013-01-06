# coding=utf8
import textwrap
import unittest

from greglink.models import testfile
from mock import patch
from StringIO import StringIO


class TestExtractHeader(unittest.TestCase):

    def test_extract_header_empty_file(self):
        expected = ""
        mockfile = StringIO("")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

    def test_extract_header_no_header_in_file(self):
        expected = ""
        mockfile = StringIO("foobar\nfoobar\nfoobar")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

    def test_extract_header_with_only_one_delimiter(self):
        expected = ""
        mockfile = StringIO("---\n")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

    def test_extract_header_empty_header(self):
        expected = ""
        mockfile = StringIO("---\n---\n")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

    def test_extract_header_one_line(self):
        expected = "foo: bar"
        mockfile = StringIO("---\nfoo: bar\n---\n")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

    def test_extract_header_two_lines(self):
        expected = "foo: bar\nfoo2: bar2"
        mockfile = StringIO("---\nfoo: bar\nfoo2: bar2\n---\n")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

    def test_extract_header_ignore_garbage_around_header(self):
        expected = "foo: bar\nfoo2: bar2"
        mockfile = StringIO("garbage\n---\nfoo: bar\nfoo2: bar2\n---\ngarbage\n")

        result = testfile.extract_header(mockfile)
        self.assertEquals(expected, result)

class TestParseHeader(unittest.TestCase):

    def test_parse_header_empty_header(self):
        header = u""
        expected = None

        result = testfile.parse_header(header)
        self.assertEquals(expected, result)

    def test_parse_header_one_line(self):
        header = u"foo: baréé"
        expected = {u'foo': u'baréé'}

        result = testfile.parse_header(header)
        self.assertEquals(expected, result)

    def test_parse_header_two_lines(self):
        header = u"foo: baréé\nfoo2: baréé2"
        expected = {u'foo': u'baréé', u'foo2': u'baréé2'}

        result = testfile.parse_header(header)
        self.assertEquals(expected, result)

class TestExtractMarkup(unittest.TestCase):

    def test_extract_markup_encode_markup(self):
        mockfile = StringIO("éééààà")
        expected = u"éééààà"

        result = testfile.extract_markup(mockfile)
        self.assertEquals(expected, result)

class TestConvertMarkup(unittest.TestCase):

    def test_convert_markup_simple_content(self):
        mockfile = textwrap.dedent(u"""
        Hello world
        ===========

        contentééé
        """)

        expected = u"<h1>Hello world</h1>\n<p>contentééé</p>"

        result = testfile.convert_markup(mockfile)
        self.assertEquals(expected, result)

class TestLoadTestFile(unittest.TestCase):

    def test_load_testfile_empty_file(self):
        mockfile = StringIO("")
        expected = (None, "")

        result = testfile.load_testfile(mockfile)
        self.assertEquals(result, expected)

    def test_load_testfile_incomplete_header(self):
        mockfile = StringIO("---\nfoo: bar\n\n")
        expected = (None, "")

        result = testfile.load_testfile(mockfile)
        self.assertEquals(result, expected)

    def test_load_testfile_only_header(self):
        mockfile = StringIO("---\nfoo: bar\n---\n")
        expected = ({'foo': 'bar'}, "")

        result = testfile.load_testfile(mockfile)
        self.assertEquals(result, expected)

    def test_load_testfile_small_file(self):
        mockfile = StringIO(textwrap.dedent("""
        ---
        foo: bar
        ---

        Hello World
        ===========

        content
        """))

        expected = ({'foo': 'bar'}, u"Hello World\n===========\n\ncontent")

        result = testfile.load_testfile(mockfile)
        self.assertEquals(result, expected)


if __name__ == "__main__":
    unittest.main()
