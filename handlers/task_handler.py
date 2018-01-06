from google.appengine.api import urlfetch
from handlers.base_handler import BaseHandler

class FetchCoinTickerHandler(BaseHandler):
	def post(self):
		"""This endpoint will be called by a cron job."""
		#TODO(joseph) implement code to pull data and save to ndb.
		url = 'https://api.coinmarketcap.com/v1/ticker/'
		try:
			result = urlfetch.fetch(url)
			if result.status_code == 200:
				self.response.write(result.content)
			else:
				self.response.status_code = result.status_code
		except urlfetch.Error:
			logging.exception('Caught exception fetching url')
			self.error_response('ERROR FETCHING DATA!!!')


ROUTES = [
  ('/_tasks/fetch_coin_ticker', FetchCoinTickerHandler )
]