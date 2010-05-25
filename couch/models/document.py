from datetime import datetime
from google.appengine.ext import db
from django.utils import simplejson as json
from couch import errors
from couch.models.util import gen_uuid

class DocumentRoot(db.Model):
    ''' Controls document '''
    revno = db.IntegerProperty(default = 0)
    revsuffix = db.StringProperty()
    deleted = db.BooleanProperty(default = False)

    def rev(self):
        return '%s-%s' % (self.revno, self.revsuffix)

class Document(db.Model):
    id = db.StringProperty()
    rev = db.StringProperty()
    dbname = db.StringProperty()
    docstring = db.TextProperty()
    deleted = db.BooleanProperty(default = False)

    def to_dict(self):
        return json.loads(self.docstring)
