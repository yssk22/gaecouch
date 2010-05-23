# Installation

configure app.yaml copied from app.yaml.example, 
and deploy the application on your GAE environment.


## Not all APIs are completed.

A few APIs are currently supported (Database and Document APIs). 
If an API is not implemented yet, the response will be as follows.

    $ curl -X GET http://gaecouch.appspot.com/_stats
    $ {"reason": "please contribute implementation.", "error": "not_implemented"}

Welcome to fork and contribute if you are interested in!

## Example

    $ curl -X GET http://gaecouch.appspot.com/
    {"not_found": "Welcome", "version": "0.11.0"}

    $ curl -X GET http://gaecouch.appspot.com/a
    {"reason": "not_found", "error": "no_db_file"}

    $ curl -X GET http://gaecouch.appspot.com/a
    {"update_seq": 0, "purge_seq": 0, "doc_count": 0, "compact_running": false, "db_name": "a", "disk_format_version": 5, "instance_start_time": 1274547941.0, "doc_del_count": 0}

    $ curl -X PUT --data '' http://gaecouch.appspot.com/a
    {"ok": true}
    
    $ curl -X POST --data '{"foo": "bar"}' http://gaecouch.appspot.com/a
    {"rev": "1-94232c5b8fc9272f6f73a1e36eb68fcf", "ok": true, "id": "55fb77f2ea3f480d966055398a7d282a"}

    $ curl -X PUT --data '{"_rev": "1-94232c5b8fc9272f6f73a1e36eb68fcf", "foo": "bar", "hoge": "fuga"}' http://gaecouch.appspot.com/a/55fb77f2ea3f480d966055398a7d282a
    {"rev": "2-a99335d508426d4e600b45dd61d2d017", "ok": true, "id": "55fb77f2ea3f480d966055398a7d282a"}
    
    $ curl -X GET http://gaecouch.appspot.com/a/55fb77f2ea3f480d966055398a7d282a
    {"_rev": "2-a99335d508426d4e600b45dd61d2d017", "_id": "55fb77f2ea3f480d966055398a7d282a", "foo": "bar", "hoge": "fuga"}

    $ curl -X DELETE http://gaecouch.appspot.com/a/55fb77f2ea3f480d966055398a7d282a?rev=2-a99335d508426d4e600b45dd61d2d017
    {"rev": "3-a99335d508426d4e600b45dd61d2d017", "ok": true, "id": "55fb77f2ea3f480d966055398a7d282a"}

    $ curl -X GET http://gaecouch.appspot.com/a/55fb77f2ea3f480d966055398a7d282a
    {"error": "not_found", "reason": "deleted"}
    
    $ curl -X DELETE http://gaecouch.appspot.com/a
    {"ok": true}

    $ curl -X GET http://gaecouch.appspot.com/a
    {"reason": "not_found", "error": "missing"}
