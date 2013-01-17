from urlparse import urlparse
from mock import Mock
import json
from nose.tools import eq_

from memjogger.tests import Base
from memjogger.api import ErrorResponse

class TestQueryingCardSets(Base):
    def query_all_card_sets_test(self):
        api = self.get_api_handle()
        
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset':
                return Mock(status_code = 200, text = json.dumps(dict(card_sets = [dict(id = 1, name = 'cs1')])))
        self.add_request_handler('get', handler)
        
        response = api.get_card_sets()
        eq_(response.data['card_sets'], [dict(id=1, name = 'cs1')])
        eq_(response.http.status_code, 200)
        
    def query_card_set_test(self):
        api = self.get_api_handle()
        
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1':
                return Mock(status_code = 200, text = json.dumps(dict(card_set = [dict(id = 1, name = 'cs1')])))
        self.add_request_handler('get', handler)
        
        response = api.get_card_set(1)
        eq_(response.data['card_set'], [dict(id=1, name = 'cs1')])
        eq_(response.http.status_code, 200)
        
    def query_non_existing_card_set_test(self):
        api = self.get_api_handle()
        
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1':
                return Mock(status_code = 404)
        self.add_request_handler('get', handler)
        
        response = api.get_card_set(1)
        eq_(response.data, None)
        eq_(response.http.status_code, 404)