"""Utilties for writing unit tests."""
import webapp2

from google.appengine.ext import testbed
from google.appengine.ext import ndb


def test_webapp(routes):
  """Return webapp with test config."""
  config = {
    'webapp2_extras.sessions': {
      'secret_key': 'secret'
    }
  }
  return webapp2.WSGIApplication(routes, config=config)


def valid_signup_data():
  return {
    'name': 'Donald Trump',
    'username': 'presido',
    'email': 'foo@gmail.com',
    'password': '123.com',
    'country': 'US'
  }


def initialize_testbed():
  """Initialize a Testbed for use in setUp procedures."""
  tb = testbed.Testbed()
  tb.activate()
  tb.init_datastore_v3_stub()
  tb.init_memcache_stub()
  ndb.get_context().clear_cache()
  return tb
