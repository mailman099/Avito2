import hashlib
import json
import urllib
from pathlib import Path
from urllib.parse import ParseResult

from content import ContentGetter
from notification import Notificator
from parser import ContentParser


class Application:
    def __init__(self, content_getter: ContentGetter, content_parser: ContentParser, notificator: Notificator):
        self._content_getter = content_getter
        self._content_parser = content_parser
        self._notificator = notificator

        self._target_dir = Path('target')
        self._target_dir.mkdir(parents=True, exist_ok=True)

    def main(self):
        with open('resources/urls.txt', 'r') as fp:
            urls = set(filter(bool, map(str.strip, fp)))

        diffs = []
        for url in urls:
            content = self._content_getter.get_resource(url)
            current_items = self._content_parser.parse(content)

            previous_items = self._get_previous_items(url)
            if not previous_items:
                diff = current_items
            else:
                for item in previous_items:
                    try:
                        newest_from_idx = current_items.index(item)
                    except ValueError:
                        newest_from_idx = -1
                    if newest_from_idx != -1:
                        diff = current_items[:newest_from_idx]
                        break
                else:
                    diff = current_items

            if diff:
                diffs += diff
                self._save_items(url, current_items)

        if diffs:
            diffs = json.dumps(diffs, indent=2, ensure_ascii=False)
            self._notificator.notify(diffs)

    def _url_to_filename(self, url):  # type: (str) -> str
        full_query = urllib.parse.urlparse(url).query
        search_query = urllib.parse.parse_qs(full_query)['q'][0]
        return hashlib.sha256(url.encode()).hexdigest()[:8] + '_' + search_query + '.json'

    def _save_items(self, url, items):  # type: (str, list[dict]) -> None
        result = {'url': url, 'items': items}
        filename = self._url_to_filename(url)
        with (self._target_dir / filename).open(mode='w', encoding='utf-8') as fp:
            json.dump(result, fp, indent=2, ensure_ascii=False)

    def _get_previous_items(self, url):  # type: (str) -> list[dict]
        filename = self._url_to_filename(url)
        if (self._target_dir / filename).exists():
            with (self._target_dir / filename).open('r', encoding='utf-8') as fp:
                previous = json.load(fp)['items']
        else:
            previous = []
        return previous
