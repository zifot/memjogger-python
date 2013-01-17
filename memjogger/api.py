import requests
import json

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
    
    def _request(self, type, path, **kwargs):
        def call():
            return getattr(requests, type)(API_URL + path, auth = self.auth, **kwargs)
        
        response = call()
        if response.status_code == 401:
            self.authenticate()
            response = call()
        if response.status_code == 401:
            return ErrorResponse(response)
        
        body = None
        if response.text:
            body = json.loads(response.text)
        return Response(response, body)
    
    def authenticate(self):
        response = requests.post(API_URL + 'user/login', data = json.dumps(dict(email = self.email, passwd = self.password)))
        if response.status_code == 200:
            self.auth.token = json.loads(response.text)['token']
    
    def get_card_sets(self): 
        return self._request('get', 'cardset')

    def get_card_set(self, id):
        return self._request('get', 'cardset/%s' % id)
    