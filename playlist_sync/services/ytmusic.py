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

    def fetch_playlist(self, url: str, *, cache_metadata: bool = True) -> list[Track]:
        log.info(f'Fetching playlist {url}')
        result = self.api.get_playlist(url, limit=None)

        yt_tracks = result['tracks']
        total = result['trackCount']
        log.info(f'Done fetching playlist with {total} tracks, fetched {len(yt_tracks)}')

        tracks = []

        for yt_track in yt_tracks:
            artists = ', '.join(a['name'] for a in yt_track['artists'])
            track = Track(
                title=yt_track['title'],
                artist=artists,
                service=str(self),
                metadata=yt_track if cache_metadata else None,
            )
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

    def search_track(self, track: Track, *, cache_metadata: bool = True) -> str:
        log.info(f'Searching for id for {track}')
        results = self.api.search(
            query=f'{track.title} by {track.artist}', limit=1, filter='songs', ignore_spelling=True
        )

        # cache track metadata
        if cache_metadata and str(self) not in track._service_metadata:
            track._service_metadata[str(self)] = results[0]

        video_id = results[0]['videoId']
        log.info(f'Found id for {track}: {video_id}')
        return video_id

    def ensure_track_metadata(self, track: Track, *, cache_metadata: bool = True) -> str:
        if str(self) in track._service_metadata:
            # we already have the track ID for this one
            return track._service_metadata[str(self)]['videoId']
        else:
            return self.search_track_id(track, cache_metadata=cache_metadata)

    def remove_from_playlist(self, url: str, tracks: list[Track]):
        log.info('Resolving corresponding track IDs')
        track_metadata = []

        for track in tracks:
            self.resolve_track_id(track, cache_metadata=True)
            track_metadata.append(track._service_metadata[str(self)])

        log.info('Removing tracks from playlist')
        result = self.api.remove_playlist_items(url, track_metadata)
        status = result if isinstance(result, str) else result['status']

        if status != 'STATUS_SUCCEEDED':
            log.info(f'Failed to remove, status of removal: {result}')

    def add_to_playlist(self, url: str, tracks: list[Track]):
        log.info('Resolving corresponding track IDs')
        track_ids = []

        for track in tracks:
            track_ids.append(self.resolve_track_id(track))

        # remove duplicates
        track_ids = self._remove_duplicates(track_ids)

        log.info('Adding tracks to playlist')
        result = self.api.add_playlist_items(url, track_ids)
        status = result if isinstance(result, str) else result['status']

        if status != 'STATUS_SUCCEEDED':
            log.info(f'Failed to add, status of addition: {result}')
