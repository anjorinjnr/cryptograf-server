"""Data models for application."""

import time
from google.appengine.ext import ndb
from google.appengine.api import memcache
from webapp2_extras.appengine.auth.models import User as AuthUser

# alias ndb types
type_string = ndb.StringProperty
type_text = ndb.TextProperty
type_int = ndb.IntegerProperty
type_json = ndb.JsonProperty
type_float = ndb.FloatProperty
type_key = ndb.KeyProperty
type_struct = ndb.StructuredProperty
type_bool = ndb.BooleanProperty
type_date = ndb.DateProperty
type_datetime = ndb.DateTimeProperty


def not_empty(data, field):
  if not field or not data:
    return False

  if field in data and data[field]:
    return True
  else:
    return False


class BaseModel(ndb.Model):
  """Shared properties by all models."""
  created_at = type_int()
  created_by = type_key()
  modified_at = type_int()
  deleted = type_bool()
  deleted_at = type_int()

  _has_index = False

  _exclude = None

  def to_dict(self, include=None, exclude=None):
    exclude = self._exclude
    return self._to_dict(include=include, exclude=exclude)

  def _pre_put_hook(self):
    """Pre-put operations. Store UTC timestamp(s) in milliseconds."""
    now = int(time.time() * 1000)
    self.modified_at = now
    if not self.created_at:
      self.created_at = now
    if self.deleted:
      self.deleted_at = now

  def _post_put_hook(self, future):
    """Post-put operations. Store UTC timestamp(s) in milliseconds."""
    o = future.get_result().get()
    if o._has_index:
      o.update_index()


class User(AuthUser):
  """A human using the application."""
  name = type_string(required=True)
  username = type_string(required=True)
  email = type_string(required=True)
  country = type_string(required=True)
  about = type_text()
  followers = type_key(kind='User', repeated=True)
  following = type_key(kind='User', repeated=True)

  _exclude = ['password', 'auth_ids']

  @classmethod
  def get_user_by_email(cls, email):
    return cls.query(cls.email == email).get()

  def to_dict(self, include=None, exclude=None):
    exclude = self._exclude
    return self._to_dict(include=include, exclude=exclude)



class CoinPick(BaseModel):
  """A coin selected by a user, ideally an influencer, as a recommendation."""
  user = type_key(kind='User')
  expires_at = type_int()
  coin = type_key(kind='Coin')


class Coin(BaseModel):
  """A specific cryptocurrency e.g Bitcoin. """
  name = type_string(required=True)
  symbol = type_string(required=True)


class Exchange(BaseModel):
  name = type_string()
  website = type_string()


class TradeActivity(ndb.Model):
  """Specific information for a trade activity."""
  username = type_string()
  type = type_string()
  coin_symbol = type_string()
  exchange = type_string()


class ActivityData(ndb.Model):
  """Wrapper for data about different activities."""
  trade = type_struct(TradeActivity)


class Activity(BaseModel):
  """A event recorded for a shared e.g a trade."""
  activity_type = type_string()
  data = type_struct(ActivityData)


class Setting(ndb.Model):
  """Key/Value store for application settings."""
  name = type_string(required=True)
  value = type_string(required=True)

  @classmethod
  def init(cls):
    """Load settings into memcache."""
    settings = cls.query().fetch()
    for setting in settings:
      memcache.add(setting.name, setting.value)

  @classmethod
  def get(cls, key):
    data = memcache.get('key')
    if data is not None:
      return data
    else:
      setting = cls.query(Setting.name == key).get()
      if setting:
        memcache.add(setting.name, setting.value)
        return setting.value

  @classmethod
  def add(cls, key, value):
    setting = cls.query(Setting.name == key).get() or cls(name=key, value=value)
    setting.put()


class Trade(BaseModel):
  """A buy or sell of an asset i.e coin."""
  user = type_key(kind=User)
  trade_pair = type_string()
  exchange = type_key(kind=Exchange)
  trade_type = type_string()
  current_price = type_float()
  trade_price = type_float()
  quantity = type_float()
  visibility = type_string()
  total = type_float()
  notes = type_text()


class Asset(BaseModel):
  """A coin currently help user a user."""
  user = type_key(kind=User)
  trades = type_key(kind=Trade, repeated=True)
  coin = type_key(kind=Coin)
  quantity = type_float()
  current_price = type_float()


# changing events - buy, sell, price change
class Portfolio(ndb.Model):
  """All digit asset help by a user."""
  user = type_key(kind=User)
  size = type_float()
  assets = type_key(kind=Asset, repeated=True)


class PortfolioHistory(BaseModel):
  """Portfolio snapshot at point in time."""
  user = type_key(kind=User)
  portfolio = ndb.LocalStructuredProperty(Portfolio)


class CoinTicker(BaseModel):
  """A ticker contains details about a Coin at a particular point in time."""
  coin = type_key(kind=Coin, required=True)
  price_usd = type_float(required=True)
  price_btc = type_float()
  volume_usd_24h = type_float()
  market_cap_usd = type_float()
  percent_change_1h = type_float()
  percent_change_24h = type_float()
  percent_change_7d = type_float()
  available_supply = type_float()
  total_supply = type_float()
  max_supply = type_float()

  @classmethod
  def save(cls, data):
    # TODO(joseph): validate data and set other properties
    ticker = cls(name=data['name'],
                 symbol=data['symbol'],
                 price_usd=data['price_usd'])
    if not_empty(data, 'price_btc'):
      ticker.price_btc = data['price_btc']

    ticker.put()

    return ticker
