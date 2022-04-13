import time
from pathlib import Path

import schedule
from pygame import mixer

from application import Application
from content.http import HttpContentGetter
from notification import Notificator
from notification.console import ConsoleNotificator
from notification.webdriver_notificator import SeleniumNotificator
from parser.http import Bs4Parser


class NotificatorAggregator(Notificator):
    def __init__(self, *notificators):
        mixer.init()
        self._resource_dir = Path('resources')
        self._notificators = notificators

    def notify(self, new_items):
        for notify_sound in self._resource_dir.glob('notify.*'):
            mixer.music.load(notify_sound)
            mixer.music.play()
            break

        for notificator in self._notificators:
            notificator.notify(new_items)


if __name__ == '__main__':
    content_getter = HttpContentGetter()
    parser = Bs4Parser()

    console_notificator = ConsoleNotificator()
    selenium_notificator = SeleniumNotificator()
    notificator = NotificatorAggregator(console_notificator, selenium_notificator)

    first_run_app = Application(content_getter=content_getter, content_parser=parser, notificator=console_notificator)
    first_run_app.main()

    scheduled_app = Application(content_getter=content_getter, content_parser=parser, notificator=notificator)
    schedule.every(5).minutes.do(scheduled_app.main)

    while 1:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()
