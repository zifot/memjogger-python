import requests
import json
from mock import patch, Mock
from urlparse import urlparse

from memjogger.api import Handle


def login_handler(url, *args, **kwargs):
    if urlparse(url).path == '/api/user/login':
        if json.loads(kwargs['data']) == dict(email = 'test@test.com', passwd = 'passwd'):
            return Mock(status_code = 200, text = json.dumps(dict(token = 'mjtoken')))

def authentication_handler(url, *args, **kwargs):
    auth = kwargs.get('auth')
    if not auth or auth.token != 'mjtoken':
        return Mock(status_code = 401)  

        
class HandlerManager:
    def __init__(self):
        self.handlers = []
    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            ret = handler(*args, **kwargs)
            if ret is not None:
                return ret
    def add_handler(self, handler):
        self.handlers.append(handler)
        
class Base:
    def setUp(self):
        self.request_patchers = dict()
        self.request_mocks = dict()
        for to_patch in ['get', 'post', 'put', 'delete']:
            patcher = self.request_patchers[to_patch] = patch('requests.' + to_patch)        
            mock = self.request_mocks[to_patch] = patcher.start()
            mock.side_effect = HandlerManager()
            
        self.add_request_handler('post', login_handler)
        self.add_request_handler(None, authentication_handler)
        self.api = self.get_api_handle()
        
    def tearDown(self):
        for patcher in self.request_patchers.values():
            patcher.stop()

    def add_request_handler(self, request_type_filter, handler):
        types = ['get', 'post', 'put', 'delete']
        if request_type_filter:
            types = [request_type_filter]
        for type in types:
            self.request_mocks[type].side_effect.add_handler(handler)
    
    @staticmethod
    def get_api_handle(email = 'test@test.com', password = 'passwd'):
        return Handle(email = email, password = password)