import unittest
from castervoice.lib.textformat import TextFormat


class TestTextFormat(unittest.TestCase):

    def setUp(self):
        self.text_format = TextFormat(5, 3)

    def test_formatted_text(self):
        test_string = TextFormat.formatted_text(0, 0, 'this is a test')
        self.assertEqual(test_string, 'this is a test')
        test_string = TextFormat.formatted_text(1, 1, 'this is a test')
        self.assertEqual(test_string, 'THISISATEST')
        test_string = TextFormat.formatted_text(2, 2, 'this is a test')
        self.assertEqual(test_string, 'This-Is-A-Test')
        test_string = TextFormat.formatted_text(3, 3, 'this is a test')
        self.assertEqual(test_string, 'this_Is_A_Test')
        test_string = TextFormat.formatted_text(4, 4, 'this is a test')
        self.assertEqual(test_string, 'This.is.a.test')
        test_string = TextFormat.formatted_text(5, 5, 'this is a test')
        self.assertEqual(test_string, 'this/is/a/test')
        test_string = TextFormat.formatted_text(6, 6, 'tHiS Is a TeSt')
        self.assertEqual(test_string, 'tHiS\\Is\\a\\TeSt')
        test_string = TextFormat.formatted_text(7, 6, 'tHiS Is a TeSt')
        self.assertEqual(test_string, 'THiS\\Is\\a\\TeSt')
        test_string = TextFormat.formatted_text(8, 6, 'THiS Is a TeSt')
        self.assertEqual(test_string, 'tHiS\\Is\\a\\TeSt')

    def test_set_text_format(self):
        self.text_format.set_text_format(1, 2)
        test_string = self.text_format.get_formatted_text('this is a test')
        self.assertEqual(test_string, 'THIS-IS-A-TEST')
        self.text_format.set_text_format(3, 1)
        test_string = self.text_format.get_formatted_text('this is a test')
        self.assertEqual(test_string, 'thisIsATest')

    def test_clear_text_format(self):
        self.text_format.set_text_format(4, 5)
        test_string = self.text_format.get_formatted_text('this is a test')
        self.assertEqual(test_string, 'This/is/a/test')
        self.text_format.clear_text_format()
        test_string = self.text_format.get_formatted_text('this is a test')
        self.assertEqual(test_string, 'this_is_a_test')
