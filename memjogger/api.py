import requests
import json
import logging
import datetime

logger = logging.getLogger(__name__)

class Response:
    def __init__(self, http, data = None):
        self.http = http
        self.data = data
        
class ErrorResponse(Response):
    pass
    
class InvalidMarkError:
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
    
    def create_card_set(self, name):
        return self._request('post', 'cardset', data = json.dumps(dict(name = name)))
        
    def update_card_set(self, id, new_name):
        return self._request('put', 'cardset/%s' % id, data = json.dumps(dict(name = new_name)))
        
    def delete_card_set(self, id):
        return self._request('delete', 'cardset/%s' % id)
        
    def get_cards(self, card_set_id):
        return self._request('get', 'cardset/%s/cards' % card_set_id)
        
    def get_card(self, card_id):
        return self._request('get', 'card/%s' % card_id)
        
    def create_card(self, card_set_id, q, a):
        toret = self._request('post', 'cardset/%s/cards' % card_set_id, data = json.dumps(dict(q = q, a = a)))
        if toret.data and 'next_exam_date' in toret.data:
            dt = datetime.datetime.strptime(toret.data['next_exam_date'], '%Y-%m-%d')
            toret.data['next_exam_date'] = datetime.date(dt.year, dt.month, dt.day)
        return toret
        
    def update_card(self, card_id, q, a):
        return self._request('put', 'card/%s' % card_id, data = json.dumps(dict(q = q, a = a)))
        
    def delete_card(self, card_id):
        return self._request('delete', 'card/%s' % card_id)
        
    def mark_card(self, card_id, mark):
        try:
            mark = int(mark)
            assert mark >= 1 and mark <= 5
        except:
            raise InvalidMarkError

        toret =  self._request('post', 'card/%s/mark' % card_id, data = json.dumps(dict(mark = mark)))
        if toret.data and 'next_exam_date' in toret.data:
            dt = datetime.datetime.strptime(toret.data['next_exam_date'], '%Y-%m-%d')
            toret.data['next_exam_date'] = datetime.date(dt.year, dt.month, dt.day)
        return toret
        