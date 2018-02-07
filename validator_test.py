import unittest

from mock import patch

from validator import MyValidator


class MyValidatorTest(unittest.TestCase):
  def setUp(self):
    self.validator = MyValidator()

  def test_validate_email(self):
    valid_email = 'foo@service.com'
    self.assertTrue(self.validator._validate_type_email(valid_email))

    valid_email = 'foo.bar@service.com'
    self.assertTrue(self.validator._validate_type_email(valid_email))

    valid_email = 'foo.bar@service.co.uk'
    self.assertTrue(self.validator._validate_type_email(valid_email))

    valid_email = 'foo_bar_02@service.ord'
    self.assertTrue(self.validator._validate_type_email(valid_email))


    with patch('cerberus.Validator._error') as mock:
      invalid_email = 'foo'
      self.assertFalse(self.validator._validate_type_email(invalid_email))
      mock.assert_called_with('email', 'Not a valid email')
      invalid_email = 'foo@'
      self.assertFalse(self.validator._validate_type_email(invalid_email))

      self.assertEqual(2, mock.call_count)
