import webapp2
import json


from handlers import task_handler

VERSION = '0.0.3'


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

         ] + task_handler.ROUTES

app = webapp2.WSGIApplication(routes, debug=True)
