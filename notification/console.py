import time
from pathlib import Path

from pygame import mixer

from notification import Notificator


class ConsoleNotificator(Notificator):
    def __init__(self):
        self._resource_dir = Path('resources')

    def notify(self, new_items):  # type: (object) -> None
        print(new_items)
        for notify_sound in self._resource_dir.glob('notify.*'):
            mixer.init()
            mixer.music.load(notify_sound)
            mixer.music.play()
            break
