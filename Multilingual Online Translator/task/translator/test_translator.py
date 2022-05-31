import unittest
from unittest import mock
# from unittest.mock import patch
# from unittest import TestCase
import translator


class TestTranslator(unittest.TestCase):  # a test case for the translator.py module
    @mock.patch('translator.input', create=True)
    def test_get_language(self, mocked_input):
        # tests for the get_language() function
        mocked_input.side_effect = ['br', 'en', 'fr']
        self.assertEqual(translator.get_language(), ('english', 'french'))
        self.assertEqual(translator.get_language(), ('french', 'english'))

    @mock.patch('translator.input', create=True)
    def test_get_word(self, mocked_input):
        # tests for the get_word() function
        mocked_input.side_effect = ['hello']
        self.assertEqual(translator.get_word(), 'hello')

    @mock.patch('builtins.print')
    def test_print_message(self, mock_print):
        translator.print_message('english', 'hello')
        mock_print.assert_called_with('You chose "en" as a language to translate "hello".')
        translator.print_message('french', 'bye')
        mock_print.assert_called_with('You chose "fr" as a language to translate "bye".')

    def test_get_url(self):
        self.assertEqual(translator.get_url('english', 'french', 'hello'),
                         'https://context.reverso.net/translation/english-french/hello')
        self.assertEqual(translator.get_url('french', 'english', 'bye'),
                         'https://context.reverso.net/translation/french-english/bye')

    # def test_get_page(self):
    #     self.assertEqual(translator.get_page('https://context.reverso.net/translation/english-french/hello'),
    #                      '<Response [200]>')


# class TestTranslator(TestCase):  # a test case for the translator.py module
#     @patch('translator.get_language', return_value='en')
#     def test_english(self, input):
#         self.assertEqual(translator.get_language(), ('english', 'french'))
