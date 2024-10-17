# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import importlib
import logging
import pathlib
import sys

import spotipy
import ytmusicapi
from spotipy.oauth2 import SpotifyOAuth

from playlist_sync.services.spotify import Spotify
from playlist_sync.services.ytmusic import YTMusic


log = logging.getLogger('playlist_sync')


def initialize_spotify(client_id: str, client_secret: str) -> Spotify:

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        open_browser=False,
        redirect_uri='http://localhost:5000/',
        scope='playlist-read-private,playlist-read-collaborative',
    )
    return Spotify(spotipy.Spotify(auth_manager=auth_manager))


def initialize_ytmusic() -> YTMusic:
    if not pathlib.Path('./browser.json').is_file():
        ytmusicapi.setup(filepath='browser.json')

    return YTMusic(ytmusicapi.YTMusic('browser.json'))


def add_spotify_auth_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument('--client-id', help='Spotify Client ID')
    parser.add_argument('--client-secret', help='Spotify Client secret')


def resolve_spotify_auth_from_args(args: argparse.Namespace):
    if args.client_id is None or args.client_secret is None:
        # check for a config.py
        try:
            config = importlib.import_module('config')
        except ImportError:
            log.error('''Could not find Spotify client ID and secret.
                      Either provide them as arguments in the CLI or in a config.py file''')
            sys.exit(1)

        args.client_id = config.spotify_client_id
        args.client_secret = config.spotify_client_secret
