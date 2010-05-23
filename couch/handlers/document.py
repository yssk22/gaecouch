from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson as json
from couch.handlers import BaseHandler
from couch import models
from couch import errors

class Document(BaseHandler):
    def put(self, dbname, id):
        ''' GET /{dbname}/{id} : Update a document. '''
        database = self._database(dbname)
        try:
            document = json.loads(self.request.body)
        except ValueError:
            raise errors.BadRequest(reason = 'invalid UTF-8 JSON')
        
        document["_id"] = id
        document = models.Document.save(database, document)
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
        document = models.Document.save(database, document)
        self.writeln({ 'ok' : True,
                       'id' : document.id,
                       'rev' : document.rev })
        
    def _database(self, dbname):
        database = models.Database.get_by_key_name(dbname)
        if not database:
            raise errors.NotFound('no_db_file')
        return database

    def _document(self, database, id):
        document = models.Document.get(database, id)
        if not document:
            raise errors.NotFound(reason = 'missing')
        if document.deleted:
            raise errors.NotFound(reason = 'deleted')

        return document

class DesignDocument(BaseHandler):
    pass

class Attachment(BaseHandler):
    pass

