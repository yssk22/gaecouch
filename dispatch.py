from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import couch.handlers
import couch.handlers.database
import couch.handlers.document
import couch.handlers.misc
import couch.handlers.config

application = webapp.WSGIApplication(
    [(r'/', couch.handlers.misc.Welcome),
     (r'/_all_dbs', couch.handlers.database.AllDBs),
     (r'/_active_tasks', couch.handlers.misc.ActiveTasks),
     (r'/_config/?',  couch.handlers.config.Config),
     (r'/_config/([^/]+)/?', couch.handlers.config.Config),
     (r'/_config/([^/]+)/([^/]+)/?', couch.handlers.config.Config),
     (r'/_uuids',     couch.handlers.misc.Uuids),
     (r'/_replicate', couch.handlers.misc.Replicate),
     (r'/_stats', couch.handlers.misc.Stats),
     (r'/_session',  couch.handlers.misc.Session),
     (r'/([^/]+)/?', couch.handlers.database.Database),
     (r'/([^/]+)/_design/([^/]+)/?', couch.handlers.document.DesignDocument),
     (r'/([^/]+)/([^/]+)/?', couch.handlers.document.Document)],
    debug=True)

def main():
    run_wsgi_app(application)

