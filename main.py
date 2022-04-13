import time

import schedule
from application import Application
from content.http import HttpContentGetter
from notification.console import ConsoleNotificator
from parser.http import Bs4Parser

if __name__ == '__main__':
    content_getter = HttpContentGetter()
    parser = Bs4Parser()
    notificator = ConsoleNotificator()

    app = Application(content_getter=content_getter, content_parser=parser, notificator=notificator)

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
