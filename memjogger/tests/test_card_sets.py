from urlparse import urlparse
from mock import Mock
import json
from nose.tools import eq_

from memjogger.tests import Base
from memjogger.api import ErrorResponse

class TestQueryingCardSets(Base):
    def query_all_card_sets_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset':
                return Mock(status_code = 200, text = json.dumps(dict(card_sets = [dict(id = 1, name = 'cs1')])))
        self.add_request_handler('get', handler)
        
        response = self.api.get_card_sets()
        eq_(response.data['card_sets'], [dict(id=1, name = 'cs1')])
        eq_(response.http.status_code, 200)
        
    def query_card_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1':
                return Mock(status_code = 200, text = json.dumps(dict(card_set = [dict(id = 1, name = 'cs1')])))
        self.add_request_handler('get', handler)
        
        response = self.api.get_card_set(1)
        eq_(response.data['card_set'], [dict(id=1, name = 'cs1')])
        eq_(response.http.status_code, 200)
        
    def query_non_existing_card_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1':
                return Mock(status_code = 404, text = '')
        self.add_request_handler('get', handler)
        
        response = self.api.get_card_set(1)
        eq_(response.data, None)
        eq_(response.http.status_code, 404)
        
        
class TestCreatingCardSets(Base):
    def create_card_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset' and json.loads(kwargs['data']) == dict(name = 'cs1'):
                return Mock(status_code = 200, text = json.dumps(dict(id=1)))
        self.add_request_handler('post', handler)
        
        response = self.api.create_card_set('cs1')
        eq_(response.data['id'], 1)
        eq_(response.http.status_code, 200)
        
    def validation_error_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset' and json.loads(kwargs['data']) == dict(name = 'cs1'):
                return Mock(status_code = 422, text = json.dumps(dict(errors = ['card_set_already_exists'])))
        self.add_request_handler('post', handler)
        
        response = self.api.create_card_set('cs1')
        eq_(response.data, dict(errors = ['card_set_already_exists']))
        eq_(response.http.status_code, 422)

        
class TestEditingCardSets(Base):
    def edit_card_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1' and json.loads(kwargs['data']) == dict(name = 'cs2'):
                return Mock(status_code = 200, text = '')
        self.add_request_handler('put', handler)
        
        response = self.api.update_card_set(1, 'cs2')
        eq_(response.http.status_code, 200)
        
    def validation_error_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1' and json.loads(kwargs['data']) == dict(name = 'cs2'):
                return Mock(status_code = 422, text = json.dumps(dict(errors = ['card_set_already_exists'])))
        self.add_request_handler('put', handler)
        
        response = self.api.update_card_set(1, 'cs2')
        eq_(response.data, dict(errors = ['card_set_already_exists']))
        eq_(response.http.status_code, 422)
        
class TestDeletingCardSet(Base):
    def delete_card_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1':
                return Mock(status_code = 200, text = '')
        self.add_request_handler('delete', handler)
        
        response = self.api.delete_card_set(1)
        eq_(response.http.status_code, 200)
        
    def delete_non_existing_card_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1':
                return Mock(status_code = 404, text = '')
        self.add_request_handler('delete', handler)
        
        response = self.api.delete_card_set(1)
        eq_(response.http.status_code, 404)