import datetime
from urlparse import urlparse
from mock import Mock
import json
from nose.tools import eq_

from memjogger.tests import Base
from memjogger.api import ErrorResponse

class TestQueryingCards(Base):
    def query_all_cards_test(self):
        cards = [dict(q = 'q', a = 'a', id = 2, next_exam_date = '2013-01-01', card_set_id = 1)]
        resp = dict(cards = cards, pnum = 1, pcount = 1, count = 1)
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1/cards':
                return Mock(status_code = 200, text = json.dumps(resp))
        self.add_request_handler('get', handler)
        
        response = self.api.get_cards(1)
        eq_(response.data, resp)
        eq_(response.http.status_code, 200)
    
    def non_existing_set_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1/cards':
                return Mock(status_code = 404, text = '')
        self.add_request_handler('get', handler)
        
        response = self.api.get_cards(1)
        eq_(response.data, None)
        eq_(response.http.status_code, 404)
        
    def query_card_test(self):
        card = [dict(q = 'q', a = 'a', id = 1, next_exam_date = '2013-01-01', card_set_id = 2)]
        resp = dict(card = card)
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/card/1':
                return Mock(status_code = 200, text = json.dumps(resp))
        self.add_request_handler('get', handler)
        
        response = self.api.get_card(1)
        eq_(response.data, resp)
        eq_(response.http.status_code, 200)
      
    def non_existing_card_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/card/3':
                return Mock(status_code = 404, text = '')
        self.add_request_handler('get', handler)
        
        response = self.api.get_card(3)
        eq_(response.data, None)
        eq_(response.http.status_code, 404)

        
class TestCreatingCards(Base):
    def create_card_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1/cards' and json.loads(kwargs['data']) == dict(q = 'q', a = 'a'):
                return Mock(status_code = 200, text = json.dumps(dict(id = 1, next_exam_date = '2013-01-01')))
        self.add_request_handler('post', handler)
        
        response = self.api.create_card(card_set_id = 1, q = 'q', a = 'a')
        eq_(response.data, dict(id = 1, next_exam_date = datetime.date(2013, 1, 1)))
        eq_(response.http.status_code, 200)
        
    def validation_error_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1/cards' and json.loads(kwargs['data']) == dict(q = '', a = 'a'):
                return Mock(status_code = 422, text = json.dumps(dict(errors = ['empty_field'])))
        self.add_request_handler('post', handler)
        
        response = self.api.create_card(card_set_id = 1, q = '', a = 'a')
        eq_(response.data, dict(errors = ['empty_field']))
        eq_(response.http.status_code, 422)
        
class TestEditingCards(Base):
    def edit_card_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/card/1' and json.loads(kwargs['data']) == dict(a = 'a2', q = 'q2'):
                return Mock(status_code = 200, text = '')
        self.add_request_handler('put', handler)
        
        response = self.api.update_card(1, q = 'q2', a = 'a2')
        eq_(response.http.status_code, 200)
        
    def validation_error_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/card/1' and json.loads(kwargs['data']) == dict(a = '', q = 'q2'):
                return Mock(status_code = 422, text = json.dumps(dict(errors = ['empty_field'])))
        self.add_request_handler('put', handler)
        
        response = self.api.update_card(1, q = 'q2', a = '')
        eq_(response.data, dict(errors = ['empty_field']))
        eq_(response.http.status_code, 422)
        