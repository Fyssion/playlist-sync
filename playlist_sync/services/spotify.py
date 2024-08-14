# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
from typing import Any

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from playlist_sync.services.base import BaseService
from playlist_sync.track import Track

log = logging.getLogger('playlist_sync.services.spotify')


class Spotify(BaseService):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('scope', 'playlist-read-private,playlist-read-collaborative')
        kwargs.setdefault('redirect_uri', 'http://localhost:5000/')
        kwargs.setdefault('open_browser', False)
        auth_manager = SpotifyOAuth(*args, **kwargs)
        self.api = spotipy.Spotify(auth_manager=auth_manager)

    FETCH_PLAYLIST_KWARGS: dict[str, Any] = dict(
        fields='total,limit,items(track(name))',
        additional_types=('track',),
    )

    def fetch_playlist(self, url: str) -> list[Track]:
        log.info(f'Fetching playlist {url}')
        result = self.api.playlist_items(url, **Spotify.FETCH_PLAYLIST_KWARGS)

        if result is None:
            # uh oh
            raise RuntimeError(f'Failed to fetch playlist {url} on {self}')

        items = result['items']
        total = result['total']
        limit = result['limit']

        log.info(f'Found playlist with {total} tracks, fetched {limit}')

        if total > limit:
            # we have more tracks to fetch!
            for offset in range(limit, total, limit):
                log.info(f'Fetching playlist tracks with offset {offset}')
                result = self.api.playlist_items(
                    url, offset=offset, **Spotify.FETCH_PLAYLIST_KWARGS
                )
                if result is None:
                    # uh oh again
                    raise RuntimeError(
                        f'Failed to fetch playlist {url} on {self} (offset {offset})'
                    )
                items.extend(result['items'])

        log.info('Done fetching tracks')

        tracks = []

        for item in items:
            sp_track = item['track']
            track = Track(
                title=sp_track['name'], artist='', service=str(self), metadata=item['track']
            )  # TODO: artist
            tracks.append(track)

        return tracks

    def clear_playlist(self, url: str):
        raise NotImplementedError

    def search_track_id(self, track: Track) -> str:
        raise NotImplementedError

    def remove_from_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError

    def add_to_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError
