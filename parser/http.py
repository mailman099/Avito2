from bs4 import BeautifulSoup

from parser import ContentParser

if False:  # type hinting
    from bs4 import Tag, ResultSet  # noqa


class Bs4Parser(ContentParser):
    def __init__(self, features='lxml'):
        self._features = features

    def parse(self, content):  # type: (str) -> list[dict]
        soup = BeautifulSoup(content, self._features)  # type: BeautifulSoup
        items = soup.find_all('div', {'data-marker': 'item'})  # type: ResultSet
        result = []
        for item in items:  # type: Tag
            name = item.find('h3', {'itemprop': 'name'}).text  # type: str
            href = item.find('a', {'data-marker': 'item-title'})['href']  # type: str
            url = 'https://www.avito.ru' + href  # type: str
            result.append({'name': name, 'url': url})
        return result
