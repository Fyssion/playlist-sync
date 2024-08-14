# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import pathlib

import spotipy
import ytmusicapi
from rich.logging import RichHandler
from spotipy.oauth2 import SpotifyOAuth

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
    ytmusicapi.setup(filepath='browser.json')

auth_manager = SpotifyOAuth(
    client_id=config.spotify_client_id,
    client_secret=config.spotify_client_secret,
    open_browser=False,
    redirect_uri='http://localhost:5000/',
    scope='playlist-read-private,playlist-read-collaborative',
)
yt = YTMusic(ytmusicapi.YTMusic('browser.json'))
sp = Spotify(spotipy.Spotify(auth_manager=auth_manager))

playlist = Playlist.fetch_from(sp, config.sync_from_url)
playlist.sync_to(yt, config.sync_to_id)
