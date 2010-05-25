import time
import hashlib
from datetime import datetime
from google.appengine.ext import db
from django.utils import simplejson as json
from couch.models.document import Document, DocumentRoot
from couch.models.util import *

class Database(db.Model):
    # CouchDB properties
    disk_format_version = db.IntegerProperty(default = 5)
    update_seq = db.IntegerProperty(default = 0)
    purge_seq = db.IntegerProperty(default = 0)
    doc_count = db.IntegerProperty(default = 0)
    doc_del_count = db.IntegerProperty(default = 0)
    compact_running = db.BooleanProperty(default = False)
    instance_start_time = db.DateTimeProperty(auto_now_add = True)
    disk_size = db.IntegerProperty(default = 0)

    def to_dict(self):
        dict = {}
        dict['db_name'] = self.key().name()
        for (key, prop) in self.properties().items():
            val = prop.get_value_for_datastore(self)
            if isinstance(val, datetime):
                val = time.mktime(val.timetuple())
            dict[key] = val
        return dict

    def save(self, raw_document):
        ''' save the raw document and returns Document entity'''
        return self._save(raw_document)

    def bulk_save(self, raw_docs, all_or_nothing = False):
        ''' save bulk documents and returns a list of Document entities'''
        return [self.save(raw_doc) for raw_doc in raw_docs]

    @property
    def dbname(self):
        ''' Returns the database name '''
        return self.key().name()

    def _save(self, document):
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

        docstring = json.dumps(document)
        return db.run_in_transaction(self._save_doc_transaction, id, rev, deleted, document, docstring)
    
    
    def _save_doc_transaction(self, id, rev, deleted, document, docstring):
        dbname = self.dbname
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

    def get(self, id):
        GQL = 'SELECT * FROM Document WHERE dbname = :1 AND id = :2 ORDER BY rev DESC'
        query = db.GqlQuery(GQL, self.key().name(), id)
        return query.get()
