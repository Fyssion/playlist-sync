# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import logging

from rich.logging import RichHandler

from . import spotify_to_yt, yt_to_spotify

log = logging.getLogger('playlist_sync')

logging.getLogger().setLevel(logging.INFO)
sh = RichHandler(show_time=False)
sh.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logging.getLogger().addHandler(sh)


def main():
    parser = argparse.ArgumentParser(
        prog='playlist_sync', description='Sync playlists between streaming services'
    )
    parser.set_defaults(callback=None)
    parsers = parser.add_subparsers(title='subcommands')

    spotify_to_yt.initialize(parsers)
    yt_to_spotify.initialize(parsers)

    args = parser.parse_args()

    if args.callback:
        args.callback(args)
    else:
        parser.print_help()
