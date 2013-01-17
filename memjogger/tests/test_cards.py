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
        card = [dict(q = 'q', a = 'a', id = 2, next_exam_date = '2013-01-01', card_set_id = 1)]
        resp = dict(card = card)
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1/cards/2':
                return Mock(status_code = 200, text = json.dumps(resp))
        self.add_request_handler('get', handler)
        
        response = self.api.get_card(1, 2)
        eq_(response.data, resp)
        eq_(response.http.status_code, 200)
      
    def non_existing_card_test(self):
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset/1/cards/3':
                return Mock(status_code = 404, text = '')
        self.add_request_handler('get', handler)
        
        response = self.api.get_card(1, 3)
        eq_(response.data, None)
        eq_(response.http.status_code, 404)
