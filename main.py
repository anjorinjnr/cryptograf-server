import webapp2
import json
import logging

VERSION = '0.0.1'


class BaseHandler(webapp2.RequestHandler):
  def write_response(self, data):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))


class MetricsHandler(BaseHandler):
  def healthz(self):
    self.write_response({'status': 'up', 'version': VERSION})

Route = webapp2.Route

routes = [
           Route(r'/v1/healthz',
                 handler=MetricsHandler,
                 handler_method='healthz',
                 methods=['GET'])

         ]

app = webapp2.WSGIApplication(routes, debug=True)
