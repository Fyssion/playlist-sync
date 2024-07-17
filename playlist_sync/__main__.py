# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import pathlib

from rich.logging import RichHandler

import config
from playlist_sync.playlist import Playlist
from playlist_sync.services.spotify import Spotify
from playlist_sync.services.ytmusic import YTMusic

log = logging.getLogger('playlist_sync')

logging.getLogger().setLevel(logging.INFO)
sh = RichHandler()
sh.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logging.getLogger().addHandler(sh)

if not pathlib.Path('./browser.json').is_file():
    YTMusic.setup()

yt = YTMusic('browser.json')
sp = Spotify(client_id=config.spotify_client_id, client_secret=config.spotify_client_secret)

playlist = Playlist.fetch_from(sp, config.sync_from_url)
playlist.sync_to(yt, config.sync_to_id)
