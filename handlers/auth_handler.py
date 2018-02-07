"""Endpoints for authentication into service."""
from handlers import base_handler

class AuthHandler(base_handler.BaseHandler):
  def login(self):
    pass

  def logout(self):
    self.auth.unset_session()
    return self.success_response()
