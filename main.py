"""Entry point for the web app."""
import os
import webapp2
import sys
import logging
from models import cryptograf as model
from handlers import task_handler
from handlers import user_handler
from handlers import metrics_handler

VERSION = '0.0.5'


def _IsDevEnv():
  """Returns whether we are in a development environment (non-prod)."""
  software = os.environ['SERVER_SOFTWARE']
  server = os.environ['SERVER_NAME']
  if software.lower().startswith('dev') or 'test' in server:
    return True
  return False


def _IsLocalEnv():
  """Returns whether we are in a local environment."""
  return not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def _getSecretKey():
  """Returns secret key."""
  if _IsLocalEnv():
    return os.getenv('CRYPT_AUTH_SECRET_KEY', 'super-secret')
  else:
    secret_key = model.Setting.get('auth_secret_key')
    if secret_key:
      return secret_key.encode('utf-8')
    else:
      error_msg = 'Unable to start. Missing setting auth_secret_key'
      logging.error(error_msg)
      sys.exit(error_msg)


# Configuration values,
# see https://webapp2.readthedocs.io/en/latest/guide/app.html#initialization
APP_CONFIG = {
  'webapp2_extras.sessions': {
    'secret_key': _getSecretKey()
  },
  'webapp2_extras.auth': {
    'user_model': 'models.cryptograf.User',
    'user_attributes': ['email']
  }
}

# Add all routes here.
routes = metrics_handler.ROUTES + task_handler.ROUTES + user_handler.ROUTES

logging.info('Starting App...')


def root(request, *args, **kwargs):
  return webapp2.Response(
    'Server: %s, Version: %s' % (os.environ['SERVER_NAME'], VERSION))


routes.append((r'/', root))

app = webapp2.WSGIApplication(routes, config=APP_CONFIG,
                              debug=_IsDevEnv() or _IsLocalEnv())
