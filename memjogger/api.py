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
    
    def authenticate(self):
        response = requests.post(API_URL + 'user/login', data = json.dumps(dict(email = self.email, passwd = self.password)))
        if response.status_code == 200:
            self.auth.token = json.loads(response.text)['token']
    
    def get_card_sets(self):
        def call():
            return requests.get(API_URL + 'cardset', auth = self.auth)
        
        response = call()
        if response.status_code == 401:
            self.authenticate()
            response = call()
        if response.status_code == 401:
            return ErrorResponse(response)
        
        return Response(response, json.loads(response.text))
        
    def get_card_set(self, id):
        def call():
            return requests.get(API_URL + ('cardset/%s' % id), auth = self.auth)
        
        response = call()
        if response.status_code == 401:
            self.authenticate()
            response = call()
        if response.status_code == 401:
            return ErrorResponse(response)
        
        body = None
        if response.status_code != 404:
            body = json.loads(response.text)
            
        return Response(response, body)
    