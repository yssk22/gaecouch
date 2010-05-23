''' Provides misc handlers
'''
from couch.handlers import BaseHandler
from couch import models
from couch import errors

class Welcome(BaseHandler):
    def get(self):
        ''' GET / '''
        self.writeln({
                'couchdb' : "Welcome",
                'version' : '0.11.0'
                })

class Uuids(BaseHandler):
    def get(self):
        ''' GET /_uuids{?count=N} '''
        try:
            count = int(self.request.get('count', '1'))
            if count < 0:
                raise errors.HttpError(reason = 'function_clause')
            self.writeln({'uuids': models.gen_uuid(count)})
        except ValueError:
            raise errors.HttpError(reason = 'badarg')

class Replicate(BaseHandler):
    pass

class Stats(BaseHandler):
    pass

class Session(BaseHandler):
    pass

class ActiveTasks(BaseHandler):
    pass
