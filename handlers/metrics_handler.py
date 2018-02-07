"""Endpoint to surface application metrics."""

import webapp2

from handlers.base_handler import BaseHandler
from main import VERSION


class MetricsHandler(BaseHandler):
  def healthz(self):
    self.write_response({'status': 'up', 'version': VERSION})


ROUTES = [
  webapp2.Route(r'/v1/healthz',
                handler=MetricsHandler,
                handler_method='healthz',
                methods=['GET'])

]
