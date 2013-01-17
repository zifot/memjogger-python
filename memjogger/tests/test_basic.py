from urlparse import urlparse
from mock import Mock
import json
from nose.tools import eq_

from memjogger.tests import Base
from memjogger.api import ErrorResponse


class TestAuthentication(Base):
    def invalid_credentials_test(self):
        api = self.get_api_handle(password = 'invalid_passwd')
        response = api.get_card_sets()
        assert isinstance(response, ErrorResponse)
        eq_(response.http.status_code, 401)
        
    def valid_credentials_test(self):
        api = self.get_api_handle()
        
        def handler(url, *args, **kwargs):
            if urlparse(url).path == '/api/cardset':
                return Mock(status_code = 200, text = json.dumps(dict(card_sets = [dict(id = 1, name = 'cs1')])))
        self.add_request_handler('get', handler)
        
        response = api.get_card_sets()
        eq_(response.data['card_sets'], [dict(id=1, name = 'cs1')])
        eq_(response.http.status_code, 200)