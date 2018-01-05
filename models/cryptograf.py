
import time
from google.appengine.ext import ndb

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
  created_at = type_int()
  created_by = type_key()
  modified_at = type_int()
  deleted = type_bool()
  deleted_at = type_int()

  _has_index = False

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


class CoinTicker(BaseModel):
  """A ticker contains details about a Coin at a particular point in time."""
  name = type_string(required=True)
  symbol = type_string(required=True)
  price_usd = type_float(required=True)
  price_btc = type_float()
  volume_usd_24h= type_float()
  market_cap_usd = type_float()
  percent_change_1h = type_float()
  percent_change_24h = type_float()
  percent_change_7d = type_float()
  available_supply = type_float()
  total_supply = type_float()
  max_supply = type_float()

  @classmethod
  def save(cls, data):
    #TODO(joseph): validate data and set other properties
    ticker = cls(name=data['name'],
                 symbol=data['symbol'],
                 price_usd=data['price_usd'])
    if not_empty(data, 'price_btc'):
      ticker.price_btc = data['price_btc']

    ticker.put()

    return ticker

