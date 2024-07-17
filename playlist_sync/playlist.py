# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
from typing import Self

from playlist_sync.services.base import BaseService
from playlist_sync.track import Track

log = logging.getLogger('playlist_sync.playlist')


class Playlist:
    tracks: list[Track]
    source: str

    def __init__(self, tracks: list[Track] | None = None, source: str = "<unknown>"):
        self.tracks = tracks or []
        self.source = source

    @classmethod
    def fetch_from(cls, service: BaseService, url: str) -> Self:
        tracks = service.fetch_playlist(url)
        return cls(tracks=tracks, source=str(service))

    def sync_to(self, service: BaseService, url: str):
        log.info(f'Syncing playlist to {url} on {service}')

        # TODO: remove after finishing actual syncing logic below
        log.info(f'Clearing playlist {url} on {service}')
        service.clear_playlist(url)

        tracks = service.fetch_playlist(url)
        diff = set(self.tracks) ^ set(tracks)

        to_add = []
        to_remove = []

        for track in diff:
            if track in tracks:
                # track is not in original playlist, must be removed
                to_remove.append(track)
            else:
                # track is in the original but not synced, must be added
                to_add.append(track)

        if to_add:
            log.info(f'Found {len(to_add)} tracks to add: {to_add}')
            service.add_to_playlist(url, to_add)

        if to_remove:
            log.info(f'Found {len(to_remove)} tracks to remove: {to_remove}')
            service.remove_from_playlist(url, to_remove)

        log.info('Done syncing')

    def __repr__(self) -> str:
        return f'Playlist(tracks={self.tracks!r}, source={self.source!r})'
