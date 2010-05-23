import logging
import uuid
import time
import hashlib
from datetime import datetime
from google.appengine.ext import db
from django.utils import simplejson as json
from couch import errors

def gen_uuid(count = 1):
    # TODO: support uuid1 and sequencial uuid
    return [''.join(uuid.uuid4().__str__().split('-')) for i in range(count)]


class Database(db.Model):
    # CouchDB properties
    disk_format_version = db.IntegerProperty(default = 5)
    update_seq = db.IntegerProperty(default = 0)
    purge_seq = db.IntegerProperty(default = 0)
    doc_count = db.IntegerProperty(default = 0)
    doc_del_count = db.IntegerProperty(default = 0)
    compact_running = db.BooleanProperty(default = False)
    instance_start_time = db.DateTimeProperty(auto_now_add = True)

    def to_dict(self):
        dict = {}
        dict['db_name'] = self.key().name()
        for (key, prop) in self.properties().items():
            val = prop.get_value_for_datastore(self)
            if isinstance(val, datetime):
                val = time.mktime(val.timetuple())
            dict[key] = val
        return dict


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

    @staticmethod
    def get(database, id):
        GQL = 'SELECT * FROM Document WHERE dbname = :1 AND id = :2 ORDER BY rev DESC'
        query = db.GqlQuery(GQL, database.key().name(), id)
        return query.get()

    @staticmethod
    def save(database, document):
        if document.has_key('_id'):
            id = document.get('_id')
            del document['_id']
        else:
            id = gen_uuid()[0]
        
        if document.has_key('_rev'):
            rev = document.get('_rev')
            del document['_rev']
        else:
            rev = None

        if document.has_key('_deleted'):
            deleted = document.get('_deleted') == True
            del document['_deleted']
        else:
            deleted = False

        dbname = database.key().name()
        docstring = json.dumps(document)
        return db.run_in_transaction(Document._save_transaction, dbname, id, rev, deleted, document, docstring)
    
    @staticmethod
    def _save_transaction(dbname, id, rev, deleted, document, docstring):
        # get current document
        docroot = DocumentRoot.get_by_key_name("%s/%s" % (dbname, id))
        if not docroot:
            docroot = DocumentRoot(key_name = "%s/%s" % (dbname, id))

        if docroot.deleted:
            raise errors.NotFound(reason = 'deleted')

        if docroot.revno > 0:
            if not rev:
                raise errors.Conflict(reason = 'Document update conflict.')
            try:
                revno, revsuffix = rev.split('-')
            except ValueError:
                raise errors.BadRequest(reason = 'Invalid rev format')
            if docroot.revno != int(revno) or docroot.revsuffix != revsuffix:
                raise errors.Conflict(reason = 'Document update conflict.')
            

        # save the docroot and document entity
        docroot.revno = docroot.revno + 1
        docroot.revsuffix = hashlib.md5(docstring).hexdigest()
        docroot.deleted = deleted

        document['_id'] = id
        document['_rev'] = docroot.rev()

        entity = Document(parent = docroot)
        entity.id = document['_id']
        entity.rev = document['_rev']
        entity.dbname = dbname
        entity.deleted = deleted
        entity.docstring = json.dumps(document) # use pickle?

        docroot.put()
        entity.put()
        return entity
