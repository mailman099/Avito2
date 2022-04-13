from pathlib import Path

from notification import Notificator


class ConsoleNotificator(Notificator):
    def __init__(self):
        self._resource_dir = Path('resources')

    def notify(self, new_items):  # type: (object) -> None
        print(new_items)
