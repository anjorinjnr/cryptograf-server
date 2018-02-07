"""Handles endpoints for users."""

import webapp2

from errors import UserAlreadyExistError, DataValidationError
from handlers import base_handler
from services.user_service import UserService

class UserHandler(base_handler.BaseHandler):
  @webapp2.cached_property
  def user_service(self):
    return UserService()



  def post(self):
    data = self.request_data()
    if 'id' in data:
      # do update
      pass
    else:
      try:
        user = self.user_service.create_user(data)

        # start new session
        self.user_service.start_sesssion(user)

        self.write_model(user)
      except UserAlreadyExistError as ex:
        self.error_response(ex.message)
      except DataValidationError as ex:
        self.error_response(ex.errors())


ROUTES = [
  (r'/v1/users', UserHandler)
]
