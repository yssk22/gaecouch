# Installation

configure app.yaml copied from app.yaml.example, 
and deploy the application on your GAE environment.

## Example

    $ curl -X GET http://gaecouch.appspot.com/
    {"couchdb": "Welcome", "version": "0.11.0"}


## Not all APIs are completed.

A few APIs are currently supported (Database and Document APIs). 
If an API is not implemented yet, the response will be as follows.

    $ curl -X GET http://gaecouch.appspot.com/_stats
    $ {"reason": "please contribute implementation.", "error": "not_implemented"}

Welcome to fork and contribute if you are interested in!
