import time
import webapp2
import json
import utils
from webapp2_extras import sessions

STATUS_ERROR = 400
STATUS_OK = 200


class BaseHandler(webapp2.RequestHandler):
  """Base class for request handlers."""
  CONTENT_JSON = 'application/json'
  CONTENT_TEXT = 'text/plain'

  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.

    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """
    return self.auth.store.user_model

  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      # print self.response
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="securecookie")

  def _get_response(self, content_type=CONTENT_JSON):
    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.response.headers['Content-Type'] = content_type
    return self.response

  def write_model(self, obj, **kwargs):
    response = self._get_response()
    response.write(utils.encode_model(obj, **kwargs))

  def write_response(self, data, status=STATUS_OK):
    response = self._get_response()
    response.out.write(json.dumps(data))
    response.set_status(status)
    return response

  def write_plain_response(self, data, status=STATUS_OK):
    response = self._get_response(self.CONTENT_JSON)
    response.out.write(data)
    response.set_status(status)
    return response

  def options(self):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Headers'] = ('Origin,'
                                                             'X-Requested-With,'
                                                             'Content-Type,',
                                                             'Accept')
    self.response.headers[
      'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

  def request_data(self):
    try:
      return json.loads(self.request.body)
    except Exception:  # pylint: disable=broad-except
      return {}

  def current_time(self):
    return int(time.time() * 1000)

  def success_response(self, data=None):
    if data:
      self.write_response({'status': 'success', 'data': data})
    else:
      self.write_response({'status': 'success'})

  def error_response(self, data):
    return self.write_response({'status': 'error', 'data': data},
                               STATUS_ERROR)
