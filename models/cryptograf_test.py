import unittest

from google.appengine.api import memcache
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from models import cryptograf as model


class BaseTest(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()
    self.testbed.init_datastore_v3_stub()
    ndb.get_context().clear_cache()

  def tearDown(self):
    self.testbed.deactivate()


class SettingTest(BaseTest):

  def test_init(self):
    self.assertIsNone(memcache.get('foo'))
    model.Setting.add('foo', 'bar')
    model.Setting.init()
    self.assertEqual('bar', memcache.get('foo'))

  def test_add(self):
    self.assertIsNone(model.Setting.get('foo'))
    model.Setting.add('foo', 'bar')
    self.assertEqual('bar', model.Setting.get('foo'))

  def test_add_overwrites(self):
    self.assertIsNone(model.Setting.get('foo'))

    model.Setting.add('foo', 'bar')
    self.assertEqual('bar', model.Setting.get('foo'))

    model.Setting.add('foo', 'baz')
    self.assertEqual('bar', model.Setting.get('foo'))

# class CoinTickerTest(BaseTest):
#   def test_save(self):
#     data = {
#       'name': 'Bitcoin',
#       'symbol': 'BTC',
#       'price_usd': 16916.9,
#       'price_btc': 1.0
#     }
#     ticker = model.CoinTicker.save(data)
#     self.assertIsNotNone(ticker)
#     self.assertIsNotNone(ticker.key.id())
#     self.assertEqual(ticker.name, 'Bitcoin')
#     self.assertEqual(ticker.symbol, 'BTC')
#     self.assertEqual(ticker.price_usd, 16916.9)
#     self.assertEqual(ticker.price_btc, 1.0)
