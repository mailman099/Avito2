import json
import os
import sys
import zipfile
from io import BytesIO
from pathlib import Path

import requests
from selenium import webdriver

from notification import Notificator


class SeleniumNotificator(Notificator):
    def __init__(self, webdriver_version='100.0.4896.60'):
        if sys.platform == 'win32':
            self._driver_path = Path('target/chromedriver.exe')
        elif sys.platform == 'darwin':
            self._driver_path = Path('target/chromedriver')
        else:
            raise OSError("Only win and mac supports")

        if not self._driver_path.exists():
            self._driver_path.parent.mkdir(parents=True, exist_ok=True)
            if sys.platform == 'win32':
                download_url = f'https://chromedriver.storage.googleapis.com/{webdriver_version}/chromedriver_win32.zip'
            else:
                download_url = f'https://chromedriver.storage.googleapis.com/{webdriver_version}/chromedriver_mac64.zip'
            resp = requests.get(download_url)
            zipdata = BytesIO(resp.content)
            with zipfile.ZipFile(zipdata, mode='r') as zp:
                zp.extractall(self._driver_path.parent)

            if sys.platform == 'darwin':
                os.chmod(self._driver_path, 755)

    def notify(self, new_items):
        new_items = json.loads(new_items)

        browser = webdriver.Chrome(str(self._driver_path))
        for index, item in enumerate(new_items, start=1):
            browser.execute_script(f"window.open('{item['url']}', 'tab{index}');")
