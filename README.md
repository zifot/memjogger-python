Python API Wrapper for Memjogger
================================

This is a simple wrapper for the Memjogger's HTTP API.

Installation
------------

    pip install https://github.com/zifot/memjogger-python.git

or

    $ git clone https://github.com/zifot/memjogger-python.git
    $ cd memjogger-python
    $ python setup.py install

Usage
-----

```python
api = Handle(email = 'your@email.com', password = 'your_password')
result = api.get_card_sets()
for cs in result.data['card_sets']:
    print cs['id'], cs['name']
```

Every API call returns an instance of the memjogger.api.Response object which
contains two attributes:

* http - a raw [requests.Request object](http://docs.python-requests.org/en/latest/user/advanced/#request-and-response-objects) representing an HTTP response;
* data - object representing JSON payload sent by the server (or None in the case of the empty response body).

For infromation about what the response data for a particular call might be, see the API documentation available at [http://memjogger.com/help/api](http://memjogger.com/help/api).

There are also some usage examples in the memjogger/examples directory.

TODO
----

* Support for sending client_date parameter
* Make the API of the lib a little more high level
* Add some more usage examples
* There is some room for refactoring