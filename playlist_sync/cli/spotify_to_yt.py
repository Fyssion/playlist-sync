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

    playlist = Playlist.fetch_from(sp, args._from)
    playlist.sync_to(yt, args.to)


def initialize(parsers: argparse._SubParsersAction):
    parser = parsers.add_parser(
        name='spotify-to-yt',
        description='Sync a playlist from Spotify to YT Music',
    )

    parser.set_defaults(callback=main)
    parser.add_argument(
        '-f',
        '--from',
        required=True,
        help='spotify url of the playlist to sync from',
        metavar='FROM_URL',
        dest='_from',
    )
    parser.add_argument(
        '-t',
        '--to',
        required=True,
        help='yt playlist id of the playlist to sync to',
        metavar='TO_ID',
    )
    add_spotify_auth_to_parser(parser)
