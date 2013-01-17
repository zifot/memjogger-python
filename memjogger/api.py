import requests
import json
import logging

logger = logging.getLogger(__name__)

class Response:
    def __init__(self, http, data = None):
        self.http = http
        self.data = data
        
class ErrorResponse(Response):
    pass

class MemjoggerAuth(requests.auth.AuthBase):
    def __init__(self, token = ''):
        self.token = token
    def __call__(self, request):
        if self.token:
            request.headers['X-Memjogger-Token'] = self.token
        return request
    def __repr__(self):
        return 'MemjoggerAuth: ' + self.token
        
API_URL = 'http://memjogger.com/api/'

class Handle:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.auth = MemjoggerAuth()
    
    def _request(self, type, path, do_auth = True, **kwargs):
        def call():
            url = API_URL + path
            logger.debug('request: %s %s, %s' % (type.upper(), url, kwargs))
            return getattr(requests, type)(url, auth = self.auth, **kwargs)
        
        response = call()
        logger.debug('response: %s %s' % (response.status_code, response.text))
        if response.status_code == 401 and do_auth:
            self.authenticate()
            response = call()
        if response.status_code == 401:
            return ErrorResponse(response)
        
        body = None
        if response.text:
            body = json.loads(response.text)
        return Response(response, body)
    
    def authenticate(self):
        response = self._request('post', 'user/login', do_auth = False, data = json.dumps(dict(email = self.email, passwd = self.password)))
        if response.http.status_code == 200:
            self.auth.token = response.data['token']
    
    def get_card_sets(self): 
        return self._request('get', 'cardset')

    def get_card_set(self, id):
        return self._request('get', 'cardset/%s' % id)
    