import logging
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson as json
from couch.handlers import BaseHandler
from couch import models
from couch import errors

class _BaseHandler(BaseHandler):
    ''' Base Handler for Document APIs '''
    def _database(self, dbname):
        database = models.Database.get_by_key_name(dbname)
        if not database:
            raise errors.NotFound('no_db_file')
        return database

    def _document(self, database, id):
        document = database.get(id)
        if not document:
            raise errors.NotFound(reason = 'missing')
        if document.deleted:
            raise errors.NotFound(reason = 'deleted')
        return document

class BulkDocs(_BaseHandler):
    def post(self, dbname):
        ''' GET /{dbname}/{id} : Update a document. '''
        database = self._database(dbname)
        try:
            document = json.loads(self.request.body)
        except ValueError, e:
            logging.info(self.request.body)
            raise errors.BadRequest(reason = 'invalid UTF-8 JSON')
        docs = document['docs']
        all_or_nothing = document.get('all_or_nothing', False)
        entities = database.bulk_save(docs, all_or_nothing = all_or_nothing)
        ret = [{'id': e.id , 'rev': e.rev} for e in entities]
        self.writeln(ret)

class Document(_BaseHandler):
    def put(self, dbname, id):
        ''' GET /{dbname}/{id} : Update a document. '''
        database = self._database(dbname)
        try:
            document = json.loads(self.request.body)
        except ValueError:
            raise errors.BadRequest(reason = 'invalid UTF-8 JSON')
        
        document["_id"] = id
        document = database.save(database, document)
        self.writeln({ 'ok' : True,
                       'id' : document.id,
                       'rev' : document.rev })

    def get(self, dbname, id):
        ''' GET /{dbname}/{id} : Get a document. '''
        database = self._database(dbname)
        document = self._document(database, id)
        self.writeln(document) # TODO passed to_dict options

    def delete(self, dbname, id):
        ''' DELETE /{dbname}/{id} : Delete a document. '''
        database = self._database(dbname)
        rev = self.request.get('rev', None)
        document = {'_id' : id, '_rev': rev, '_deleted': True}
        document = database.save(database, document)
        self.writeln({ 'ok' : True,
                       'id' : document.id,
                       'rev' : document.rev })
        
class DesignDocument(_BaseHandler):
    pass

class Attachment(_BaseHandler):
    pass

