"""Useful shared utilities."""

import json
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb



def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()


class NdbModelEncoder(json.JSONEncoder):
    """JSONEncoder class for NDB models."""

    def default(self, o):
        """Override default encoding for Model and Key objects."""
        if isinstance(o, ndb.Model):
            return model_to_dict(o)
        elif isinstance(o, ndb.Key):
            return {'kind': o.kind(), 'id': o.id()}
        else:
            return super(NdbModelEncoder, self).default(o)


def _convert_list(obj):
    lst = []
    for i in obj:
        if isinstance(i, datetime.datetime):
            lst.append(date_time_to_millis(i))
        elif isinstance(i, ndb.Key):
            lst.append(i.id())
        else:
            lst.append(i)
    return  lst


def _convert_dict(obj):
    o = {}
    for k, v in obj.iteritems():
        if isinstance(v, ndb.Key):
            # value is a key
            o[k] = v.id()
        elif isinstance(v, list):
            # value is a list, so we convert the items appropriately
            o[k] = _convert_list(v)
        elif isinstance(v, datetime.datetime):
            # value is datetime
            o[k] = date_time_to_millis(v)
        elif isinstance(v, ndb.Model):
            o[k] = model_to_dict(v)
        elif isinstance(v, dict):
            o[k] = _convert_dict(v)
        else:
            o[k] = v
    return o


def model_to_dict(o, **kwargs):
    """Converts a Model to a dict and assigns additional attributes via kwargs.

    Args:
      o: ndb.Model object
      **kwargs: arbitrary keyword values to assign as attributes of the dict.

    Returns:
      dict object
    """
    avatar = False
    if o.key.kind() == 'User' and hasattr(o, 'avatar') and o.avatar:
      o.avatar = None
      avatar = True


    obj = _convert_dict(o.to_dict())
    obj['id'] = o.key.id()
    if avatar:
        obj['avatar'] = True

    # convert and add the additional(extra) attributes
    extra = _convert_dict(kwargs)
    if extra:
        t = obj.copy()
        t.update(extra)
        return t
    else:
        return obj


def encode_model(o, **kwargs):
    """Encode a model as JSON, adding any additional attributes via kwargs."""
    if isinstance(o, ndb.Model):
        obj = model_to_dict(o, **kwargs)
    elif isinstance(o, list):
        obj = []
        for lo in o:
            if isinstance(lo, ndb.Model):
                obj.append(model_to_dict(lo, **kwargs))
            elif isinstance(o, dict):
                obj.append(_convert_dict(o))
            else:
                obj.append(lo)
    elif isinstance(o, ndb.Key):
        obj = {'kind': o.kind(), 'id': o.id()}
    elif isinstance(o, dict):
        obj = _convert_dict(o)
    else:
        obj = o
    return NdbModelEncoder().encode(obj)

def date_time_to_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0
