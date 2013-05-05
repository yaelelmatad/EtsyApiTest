import urllib
from _core import API, missing
from etsy_env import EtsyEnvSandbox, EtsyEnvProduction

try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

class EtsyV2(API):
    api_version = 'v2'

    def __init__(self, api_key='', key_file=None, method_cache=missing, 
                 etsy_env=EtsyEnvSandbox(), log=None, etsy_oauth_client=None):
        self.api_url = etsy_env.api_url
        self.etsy_oauth_client = None

        if etsy_oauth_client:
            self.etsy_oauth_client = etsy_oauth_client

        super(EtsyV2, self).__init__(api_key, key_file, method_cache, log)

    def _get_url(self, url, http_method, content_type, body):
        if self.etsy_oauth_client is not None:
            return self.etsy_oauth_client.do_oauth_request(url, http_method, content_type, body)
        return API._get_url(self, url, http_method, content_type, body)
