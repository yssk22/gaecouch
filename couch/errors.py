class HttpError(Exception):
    def __init__(self, status = 500, 
                 error = 'unknown error', 
                 reason = 'uknown'):
        self._status = status
        self._error = error
        self._reason = reason

    @property
    def status(self): 
        return self._status
    
    @property
    def error(self):
        return self._error
    
    @property
    def reason(self):
        return self._reason

class NotImplemented(HttpError):
    def __init__(self, error = 'not_implemented', reason = 'please contribute implementation.'):
        super(NotImplemented, self).__init__(501, error = error, reason = reason)

class BadRequest(HttpError):
    def __init__(self, error = 'bad_request', reason = 'bad_request'):
        super(BadRequest, self).__init__(400, error = error, reason = reason)

class NotFound(HttpError):
    def __init__(self, error = 'not_found', reason = 'not_found'):
        super(NotFound, self).__init__(404, error = error, reason = reason)

class Conflict(HttpError):
    def __init__(self, error = 'conflict', reason = 'conflict'):
        super(Conflict, self).__init__(409, error = error, reason = reason)

class PreconditionFailed(HttpError):
    def __init__(self, error, reason):
        super(PreconditionFailed, self).__init__(412, error, reason)
