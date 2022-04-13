import socket
import requests
from fake_useragent import UserAgent

from content import ContentGetter


class HttpContentGetter(ContentGetter):
    def __init__(self):
        self._ua = UserAgent()
        self._session = requests.Session()

    def _is_proxy_available(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('localhost', 8080))
        finally:
            sock.close()
        return result == 0

    def get_resource(self, url):  # type: (str) -> str
        headers = {'User-agent': self._ua.random}
        if self._is_proxy_available():
            proxies = {'http': 'http://localhost:8080', 'https': 'https://localhost:8080'}
            resp = self._session.get(url, headers=headers, proxies=proxies, verify='resources/public.pem')  # type: requests.Response
        else:
            resp = self._session.get(url, headers=headers)  # type: requests.Response
        return resp.text
