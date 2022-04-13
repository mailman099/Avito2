import json
import zipfile
from io import BytesIO
from pathlib import Path

import requests
from pygame import mixer
from selenium import webdriver

from notification import Notificator


class SeleniumNotificator(Notificator):
    def __init__(self, webdriver_version='100.0.4896.60'):
        self._resource_dir = Path('resources')
        self._driver_path = Path('target/chromedriver.exe')

        if not self._driver_path.exists():
            self._driver_path.parent.mkdir(parents=True, exist_ok=True)
            download_url = f'https://chromedriver.storage.googleapis.com/{webdriver_version}/chromedriver_win32.zip'
            resp = requests.get(download_url)
            zipdata = BytesIO(resp.content)
            with zipfile.ZipFile(zipdata, mode='r') as zp:
                zp.extractall(self._driver_path.parent)

    def notify(self, new_items):
        for notify_sound in self._resource_dir.glob('notify.*'):
            mixer.init()
            mixer.music.load(notify_sound)
            mixer.music.play()
            break

        new_items = json.loads(new_items)

        it = iter(new_items)
        item = next(it)
        browser = webdriver.Chrome(str(self._driver_path))
        browser.get(item['url'])
        for index, item in enumerate(it, start=2):
            browser.execute_script(f"window.open('about:blank', 'tab{index}');")
            browser.switch_to.window(f'tab{index}')
            browser.get(item['url'])
