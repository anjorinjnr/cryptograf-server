"""Handle user related logic."""

import webapp2
from webapp2_extras import auth
from errors import UserAlreadyExistError, DataValidationError

from validator import MyValidator

USER_SCHEMA = {
  'name': {
    'type': 'string',
    'empty': False,
    'required': True
  },
  'username': {
    'type': 'string',
    'empty': False,
    'required': True
  },
  'email': {
    'type': 'email',
    'empty': False,
    'required': True
  },
  'password': {
    'type': 'string',
    'empty': False,
    'minlength': 6
  },
}

validator = MyValidator()
validator.allow_unknown = True


class UserService(object):
  @webapp2.cached_property
  def auth(self):
    """Shortcut to access the auth instance as a property."""
    return auth.get_auth()

  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.

    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """
    return self.auth.store.user_model

  def start_sesssion(self, user):
    """Start new session for user.

    :param user: The User model instance
    """
    self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

  def create_user(self, user_data):
    if not validator.validate(user_data, USER_SCHEMA):
      raise DataValidationError(validator.errors)

    resp = self.user_model.create_user(user_data['email'],
                                       ['username'],
                                       email=user_data['email'],
                                       name=user_data['name'],
                                       username=user_data[
                                         'username'],
                                       country=user_data['country'],
                                       password_raw=user_data[
                                         'password'],
                                       verified=True)

    if resp[0]:
      return resp[1]
    else:
      raise UserAlreadyExistError()
