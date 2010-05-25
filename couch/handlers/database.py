import logging
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson as json
from couch.handlers import BaseHandler
from couch import models
from couch import errors

class AllDBs(BaseHandler):
    def get(self):
        q = models.Database.all()
        list = [l.key().name() for l in q]
        self.writeln(list)

class Database(BaseHandler):
    ''' database handler 
    '''
    def get(self, dbname):
        ''' GET /{dbname} : Get database info. '''
        database = models.Database.get_by_key_name(dbname)
        if database:
            self.writeln(database)
        else:
            raise errors.NotFound('no_db_file')

    def post(self, dbname):
        database = models.Database.get_by_key_name(dbname)
        if not database:
            raise errors.NotFound('no_db_file')
        try:
            document = json.loads(self.request.body)
        except ValueError, e:
            logging.info(e)
            raise errors.BadRequest(reason = 'invalid UTF-8 JSON')
        document = database.save(document)
        self.writeln({ 'ok' : True,
                       'id' : document.id,
                       'rev' : document.rev })

    def put(self, dbname):
        ''' PUT /{dbname} : Create a database. '''
        def _trans():
            database = models.Database.get_by_key_name(dbname)
            if database:
                raise errors.PreconditionFailed(error = "file_exists",
                                                reason = "The database could not be created, the file already exists.")
            database = models.Database(key_name= dbname)
            database.put()

        db.run_in_transaction(_trans)
        self.writeln({'ok': True})

    def delete(self, dbname):
        ''' DELETE /{dbname} : Delete a database '''
        def _trans():
            database = models.Database.get_by_key_name(dbname)
            if database:
                # TODO: all related document entities should be deleted.
                database.delete()
            else:
                raise errors.NotFound('missing')
        db.run_in_transaction(_trans)
        self.writeln({'ok': True})
