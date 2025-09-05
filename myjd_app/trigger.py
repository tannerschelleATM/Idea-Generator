#!/usr/bin/env python3
"""Send channel URLs to a remote JDownloader instance via MyJDownloader API.

The script reads a list of Instagram or YouTube profile/channel URLs from a
text file and instructs a remote JDownloader client to parse and download any
new videos. Credentials and device information are read from environment
variables so they are not hardcoded in the script.
"""
from myjdapi import MyJDAPI
import os

EMAIL = os.environ.get("MYJD_EMAIL")
PASSWORD = os.environ.get("MYJD_PASSWORD")
DEVICE_NAME = os.environ.get("MYJD_DEVICE")
URL_LIST = os.environ.get("CHANNELS_FILE", "channels.txt")


def main():
    with open(URL_LIST) as f:
        links = [line.strip() for line in f if line.strip()]
    jd = MyJDAPI()
    jd.connect(EMAIL, PASSWORD)
    device = jd.get_device(DEVICE_NAME)
    device.linkgrabber.add_links({"links": "\n".join(links), "autostart": True})


if __name__ == "__main__":
    main()
