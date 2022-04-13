import time

import schedule
from application import Application
from content.http import HttpContentGetter
from notification import Notificator
from notification.console import ConsoleNotificator
from notification.webdriver_notificator import SeleniumNotificator
from parser.http import Bs4Parser


class NotificatorAggregator(Notificator):
    def __init__(self, *notificators):
        self._notificators = notificators

    def notify(self, new_items):
        for notificator in self._notificators:
            notificator.notify(new_items)


if __name__ == '__main__':
    content_getter = HttpContentGetter()
    parser = Bs4Parser()

    console_notificator = ConsoleNotificator()
    selenium_notificator = SeleniumNotificator()
    notificator = NotificatorAggregator(console_notificator, selenium_notificator)

    app = Application(content_getter=content_getter, content_parser=parser, notificator=notificator)

    app.main()
    schedule.every(5).minutes.do(app.main)

    while 1:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        schedule.run_pending()
