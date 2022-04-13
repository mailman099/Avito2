from pathlib import Path

from notification import Notificator
import json


class ConsoleNotificator(Notificator):
    def __init__(self):
        self._resource_dir = Path('resources')

    def notify(self, new_items):  # type: (list[dict]) -> None
        print(json.dumps(new_items, indent=2, ensure_ascii=False))
