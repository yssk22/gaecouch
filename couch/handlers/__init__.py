import traceback
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson as json
from couch import errors

class BaseHandler(webapp.RequestHandler):
    ''' base handler class that supports REST/JSON APIs.
    '''
    def initialize(self, request, response):
        super(BaseHandler, self).initialize(request, response)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'

    def head(self, *args, **kwargs):
        raise errors.NotImplemented()

    def get(self, *args, **kwargs):
        raise errors.NotImplemented()

    def put(self, *args, **kwargs):
        raise errors.NotImplemented()

    def post(self, *args, **kwargs):
        raise errors.NotImplemented()

    def delete(self, *args, **kwargs):
        raise errors.NotImplemented()

    def trace(self, *args, **kwargs):
        raise errors.NotIpmlemented()
    
    def options(self, *args, **kwargs):
        raise errors.NotImplemented()

    def handle_exception(self, e, debug_mode):
        if isinstance(e, errors.HttpError):
            self.error(e.status)
            self.writeln({
                    "error": e.error,
                    "reason": e.reason
                    })
        else:
            if not debug_mode:
                self.error(500)
                self.writeln({
                        "error": 'unknown',
                        "reason": traceback.format_exc()
                        })
            else:
                raise Exception(traceback.format_exc())

    def write(self, obj):
        ''' utility to write object as json '''
        if hasattr(obj, 'to_dict'):
            self.response.out.write(json.dumps(obj.to_dict()))
        else:
            self.response.out.write(json.dumps(obj))

    def writeln(self, obj):
        ''' write with newline'''
        self.write(obj)
        self.response.out.write("\n")
