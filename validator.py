"""Custom Data Validators. """

from cerberus import Validator
import re

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')


class MyValidator(Validator):
  def _validate_type_email(self, value):
    """ Ensure value is a valid `email`.
     @param value: field value.
     """
    if not value or not EMAIL_REGEX.match(value):
      self._error('email', 'Not a valid email')
      return False
    return True
