import unittest

import mock
from mock import patch
import webapp2

from google.appengine.ext import testbed
from google.appengine.ext import ndb
from webapp2_extras import auth
from services.user_service import UserService
import os
from models import cryptograf as model
from errors import UserAlreadyExistError, DataValidationError

os.environ['APPLICATION_ID'] = 'TEST'


class UserServiceTest(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()
    self.testbed.init_datastore_v3_stub()
    ndb.get_context().clear_cache()
    self.user_service = UserService()

  def test_fail_create_user_invalid_data(self):
    data = {
      'name': 'Donald Trump',
      'username': 'presido',
      'country': 'US',
      'password': '',
    }
    with self.assertRaises(DataValidationError) as cm:
      self.user_service.create_user(data)
      print ex.errors()

    error = cm.exception
    self.assertItemsEqual(['email', 'password'], error.fields())

  def test_create_user(self):
    request = webapp2.Request.blank('/')
    request.app = webapp2.WSGIApplication()
    auth_instance = auth.get_auth(request=request)

    data = {
      'name': 'Donald Trump',
      'username': 'presido',
      'email': 'foo@gmail.com',
      'password': '123.com',
      'country': 'US'
    }

    with patch('webapp2_extras.auth.get_auth') as mock:
      mock.return_value = auth_instance
      self.user_service.create_user(data)
      user = model.User.get_by_auth_id('foo@gmail.com')
      self.assertEqual(user.name, 'Donald Trump')
      self.assertEqual(user.username, 'presido')
      self.assertEqual(user.country, 'US')

  def test_create_user_no_duplicates(self):
    request = webapp2.Request.blank('/')
    request.app = webapp2.WSGIApplication()
    auth_instance = auth.get_auth(request=request)

    data = {
      'name': 'Donald Trump',
      'username': 'presido',
      'email': 'foo@gmail.com',
      'password': '123.com',
      'country': 'US'
    }

    with patch('webapp2_extras.auth.get_auth') as mock:
      mock.return_value = auth_instance
      self.user_service.create_user(data)

      self.assertEqual(1, len(model.User.query().fetch()))

      # confirm no duplicate email
      with self.assertRaises(UserAlreadyExistError):
        self.user_service.create_user(data)

        # confirm no duplicate username
        with self.assertRaises(UserAlreadyExistError):
          # change email
          data['email'] = 'bar@gmail.com'
          self.user_service.create_user(data)
