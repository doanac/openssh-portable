#!/usr/bin/python3

import logging
import os
import sys
import time

from pathlib import Path

import requests

logging.basicConfig(
    level='INFO', format='%(asctime)s %(levelname)s: %(message)s')

TWENTY_MINUTES = 20 * 60
TOKEN = sys.argv[1]
HOME = Path.home()


def sync(token):
    logging.info("Sync ssh public keys for devices")
    sshdir = HOME / ".ssh"
    if not sshdir.is_dir():
        logging.warning("Creating ssh config directory: %s", sshdir)
        sshdir.mkdir()

    # TODO pagination
    headers = {"OSF-TOKEN": token}
    params = {"pubkey_format": "OpenSSH", "shared": "1"}
    r = requests.get(
        "https://api.foundries.io/ota/devices/",
        headers=headers,
        params=params)
    if r.status_code != 200:
        logging.error("Unable to get fleet public keys - HTTP_%d:\n%s",
                      r.status_code, r.text)
    with open("/tmp/authorized_keys", "w") as f:
        for d in r.json()["devices"]:
            pub = d.get('public-key')
            if pub:
                f.write('command="/rtunnel-shell %s" %s\n' % (d['name'], pub))
    os.rename("/tmp/authorized_keys", sshdir / "authorized_keys")


def loop():
    try:
        while True:
            sync(TOKEN)
            time.sleep(TWENTY_MINUTES)
    except Exception as e:
        logging.exeption(e)


# Now run loop forever making sure it recovers from unexpected exceptions
while True:
    loop()
