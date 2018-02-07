"""Custom Exceptions used in the App."""

import copy


class Error(Exception):
  """Base class for exceptions in this module."""
  pass


class UserAlreadyExistError(Error):
  """Exception raised when user already exist."""

  def __init__(self):
    self.message = 'User already exist.'


class InputError(Error):
  """Exception raised for errors in the input.

  Attributes:
      expression -- input expression in which the error occurred
      message -- explanation of the error
  """

  def __init__(self, expression, message):
    self.expression = expression
    self.message = message


class DataValidationError(Error):
  """Exception raised when data validation fails.

  Attributes:
      errors --  A dict with field names and list of associated errors.
  """

  def __init__(self, errors):
    self.__errors = errors

  def fields(self):
    """Return fields with errors."""
    return self.__errors.keys()

  def errors(self):
    """Return the errors."""
    return copy.deepcopy(self.__errors)
