# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from playlist_sync.services.base import BaseService
from playlist_sync.track import Track

if TYPE_CHECKING:
    import ytmusicapi

log = logging.getLogger('playlist_sync.services.ytmusic')


class YTMusic(BaseService):
    def __init__(self, api: ytmusicapi.YTMusic):
        self.api = api

    def fetch_playlist(self, url: str) -> list[Track]:
        log.info(f'Fetching playlist {url}')
        result = self.api.get_playlist(url, limit=None)

        yt_tracks = result['tracks']
        total = result['trackCount']
        log.info(f'Done fetching playlist with {total} tracks, fetched {len(yt_tracks)}')

        tracks = []

        for yt_track in yt_tracks:
            track = Track(
                title=yt_track['title'], artist='', service=str(self), metadata=yt_track
            )  # TODO: artist
            tracks.append(track)

        return tracks

    def clear_playlist(self, url: str):
        log.info(f'Fetching playlist {url}')
        result = self.api.get_playlist(url, limit=None)
        total = result['trackCount']
        log.info(f'Removing all {total} tracks from playlist')

        if not result['tracks']:
            log.info('No songs to clear in playlist')
            return

        result = self.api.remove_playlist_items(url, result['tracks'])
        status = result if isinstance(result, str) else result['status']

        if status != 'STATUS_SUCCEEDED':
            log.info(f'Failed to remove, status of removal: {result}')

    def search_track_id(self, track: Track) -> str:
        log.info(f'Searching for id for {track}')
        results = self.api.search(query=f'{track.title} by {track.artist}', limit=1, filter='songs', ignore_spelling=True)
        video_id = results[0]['videoId']
        log.info(f'Found id for {track}: {video_id}')
        return video_id

    def remove_from_playlist(self, url: str, tracks: list[Track]):
        # log.info('Searching for corresponding track IDs')
        # track_ids = []

        # for track in tracks:
        #     track_ids.append(self.search_track_id(track))

        # log.info('Removing tracks from playlist')
        # self.api.remove_playlist_items(url, track_ids)
        pass

    def _remove_duplicates(self, tracks: list[str]) -> list[str]:
        seen = set()
        seen_add = seen.add
        return [x for x in tracks if not (x in seen or seen_add(x))]

    def add_to_playlist(self, url: str, tracks: list[Track]):
        log.info('Searching for corresponding track IDs')
        track_ids = []

        for track in tracks:
            track_ids.append(self.search_track_id(track))

        # remove duplicates
        track_ids = self._remove_duplicates(track_ids)

        log.info('Adding tracks to playlist')
        result = self.api.add_playlist_items(url, track_ids)
        status = result if isinstance(result, str) else result['status']

        if status != 'STATUS_SUCCEEDED':
            log.info(f'Failed to add, status of addition: {result}')
