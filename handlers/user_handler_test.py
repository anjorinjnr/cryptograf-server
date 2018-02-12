import webapp2
import webtest

from unittest import TestCase

from webapp2_extras import json

import test_helper as helper

from models import cryptograf as model

from handlers.user_handler import ROUTES as routes


class UserHandlerTest(TestCase):
  def setUp(self):
    app = helper.test_webapp(routes)
    self.testapp = webtest.TestApp(app)
    self.testbed = helper.initialize_testbed()

  def tearDown(self):
    self.testbed.deactivate()

  def test_user_signup(self):
    # given
    user_data = helper.valid_signup_data()

    # when
    response = self.testapp.post('/v1/users', json.encode(user_data))

    # then
    self.assertEqual(response.status_int, 300)
    self.assertEqual(user_data['email'], response.json_body['email'])
    self.assertIsNotNone(response.json_body['id'])
    self.assertIsNotNone(response.headers['Set-Cookie'])
    self.assertIsNotNone(model.User.get_by_id(response.json_body['id']))
