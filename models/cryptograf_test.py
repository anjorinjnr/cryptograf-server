import unittest
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from models import cryptograf as model


class BaseTest(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()
    self.testbed.init_datastore_v3_stub()

class CoinTickerTest(BaseTest):

  def test_save(self):
    data = {
      'name': 'Bitcoin',
      'symbol': 'BTC',
      'price_usd': 16916.9,
      'price_btc': 1.0
    }
    ticker = model.CoinTicker.save(data)
    self.assertIsNotNone(ticker)
    self.assertIsNotNone(ticker.key.id())
    self.assertEqual(ticker.name, 'Bitcoin')
    self.assertEqual(ticker.symbol, 'BTC')
    self.assertEqual(ticker.price_usd, 16916.9)
    self.assertEqual(ticker.price_btc, 1.0)