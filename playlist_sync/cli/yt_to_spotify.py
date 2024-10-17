# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse

from playlist_sync.playlist import Playlist

from .utils import (
    add_spotify_auth_to_parser,
    initialize_spotify,
    initialize_ytmusic,
    resolve_spotify_auth_from_args,
)


def main(args: argparse.Namespace):
    resolve_spotify_auth_from_args(args)

    sp = initialize_spotify(args.client_id, args.client_secret)
    yt = initialize_ytmusic()

    playlist = Playlist.fetch_from(yt, args._from)
    playlist.sync_to(sp, args.to)


def initialize(parsers: argparse._SubParsersAction):
    parser = parsers.add_parser(
        name='yt-to-spotify',
        description='Sync a playlist from YT Music to Spotify',
    )

    parser.set_defaults(callback=main)
    parser.add_argument(
        '-f',
        '--from',
        required=True,
        help='yt playlist id of the playlist to sync from',
        dest='_from',
    )
    parser.add_argument('-t', '--to', required=True, help='spotify url of the playlist to sync to')
    add_spotify_auth_to_parser(parser)
