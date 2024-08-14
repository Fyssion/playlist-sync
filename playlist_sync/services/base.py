# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from playlist_sync.track import Track


@runtime_checkable
class BaseService(Protocol):
    def fetch_playlist(self, url: str) -> list[Track]:
        raise NotImplementedError

    def clear_playlist(self, url: str):
        raise NotImplementedError

    def search_track_id(self, track: Track) -> str:
        raise NotImplementedError

    def remove_from_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError

    def add_to_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError

    def _extract_track_metadata(self, track: Track) -> Any | None:
        return track._service_metadata.get(str(self))

    def __str__(self) -> str:
        return self.__class__.__name__
