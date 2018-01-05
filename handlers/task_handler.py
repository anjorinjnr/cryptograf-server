
from handlers.base_handler import BaseHandler

class FetchCoinTickerHandler(BaseHandler):

  def post(self):
    """This endpoint will be called by a cron job."""
    #TODO(joshua) implement code to pull data and save to ndb.

    self.error_response('NOT YET IMPLEMENTED!!!')


ROUTES = [
  ('/_tasks/fetch_coin_ticker', FetchCoinTickerHandler )
]