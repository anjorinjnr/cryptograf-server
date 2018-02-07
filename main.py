"""Entry point for the web app."""

import webapp2

from models import cryptograf as model
from handlers import task_handler
from handlers import user_handler
from handlers import metrics_handler

VERSION = '0.0.3'

## Initialize application settings.
model.Setting.init()

# Configuration values,
# see https://webapp2.readthedocs.io/en/latest/guide/app.html#initialization
APP_CONFIG = {
  'webapp2_extras.sessions': {
    'secret_key': model.Setting.get('auth_secret_key').encode('utf-8')
  },
  'webapp2_extras.auth': {
    'user_model': 'models.cryptograf.User',
    'user_attributes': ['email']
  }
}

# Add all routes here.
routes = metrics_handler.ROUTES + task_handler.ROUTES + user_handler.ROUTES

app = webapp2.WSGIApplication(routes,
                              config=APP_CONFIG,
                              debug=True)
