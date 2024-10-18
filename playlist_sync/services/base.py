# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from playlist_sync.track import Track


@runtime_checkable
class BaseService(Protocol):
    def fetch_playlist(self, url: str, *, cache_metadata: bool = True) -> list[Track]:
        raise NotImplementedError

    def clear_playlist(self, url: str):
        raise NotImplementedError

    def search_track_id(self, track: Track, *, cache_metadata: bool = True) -> str:
        raise NotImplementedError

    def resolve_track_id(self, track: Track, *, cache_metadata: bool = True) -> str:
        raise NotImplementedError

    def remove_from_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError

    def add_to_playlist(self, url: str, tracks: list[Track]):
        raise NotImplementedError

    def _extract_track_metadata(self, track: Track) -> Any | None:
        return track._service_metadata.get(str(self))

    def _remove_duplicates(self, tracks: list[str]) -> list[str]:
        seen = set()
        seen_add = seen.add
        return [x for x in tracks if not (x in seen or seen_add(x))]

    def __str__(self) -> str:
        return self.__class__.__name__
