# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import shlex
from typing import TYPE_CHECKING, Any

from playlist_sync.services.base import BaseService
from playlist_sync.track import Track

if TYPE_CHECKING:
    import spotipy

log = logging.getLogger('playlist_sync.services.spotify')


class Spotify(BaseService):
    def __init__(self, api: spotipy.Spotify):
        self.api = api

    FETCH_PLAYLIST_KWARGS: dict[str, Any] = dict(
        fields='total,limit,items(track(name,id,artists))',
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
            artists = ', '.join(a['name'] for a in sp_track['artists'])
            track = Track(
                title=sp_track['name'], artist=artists, service=str(self), metadata=sp_track
            )
            tracks.append(track)

        return tracks

    def clear_playlist(self, url: str):
        log.info(f'Fetching playlist {url}')
        tracks = self.fetch_playlist(url)

        if not tracks:
            log.info('No songs to clear in playlist')
            return

        track_ids = [t._service_metadata[str(self)]['id'] for t in tracks]
        result = self.api.playlist_remove_all_occurrences_of_items(url, track_ids)

        if result is None:
            log.info(f'Failed to remove')

    def search_track_id(self, track: Track) -> str:
        log.info(f'Searching for id for {track}')
        query = f'track:{shlex.quote(track.title)} artist:{shlex.quote(track.artist)}'
        print(query)
        result = self.api.search(query, limit=1, type='track')

        if not result or result['tracks']['total'] == 0:
            log.info('Failed to find a corresponding track id, trying with broader query')
            result = self.api.search(str(track), limit=1, type='track')

            if not result or result['tracks']['total'] == 0:
                log.info('Failed to find a corresponding song')
                raise RuntimeError('TODO')

        track_id = result['tracks']['items'][0]['id']
        log.info(f'Found id for {track}: {track_id}')
        return track_id

    def remove_from_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError

    def add_to_playlist(self, url: str, tracks: list[Track]):
        log.info('Resolving corresponding track IDs')
        track_ids = []

        for track in tracks:
            if str(self) in track._service_metadata:
                # we already have the track ID for this one
                track_ids.append(track._service_metadata[str(self)]['id'])
            else:
                track_ids.append(self.search_track_id(track))

        # remove duplicates
        track_ids = self._remove_duplicates(track_ids)

        log.info('Adding tracks to playlist')
        result = self.api.playlist_add_items(url, track_ids)

        if result is None:
            print('Failed to add tracks')
