import os

import urllib.request
from helper.twittermanager import TwitterManager

from bot import __version__


def test_version():
    assert __version__ == "0.1.0"


if __name__ == "__main__":
    # 検証したいURLを入れる
    request_url = ""

    manager = TwitterManager()
    imageurls = manager.get_image_urls(request_url)

    for url in imageurls:
        filename = os.path.basename(url)
        urllib.request.urlretrieve(url, filename)
