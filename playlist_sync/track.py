# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any


# I should've used a dataclass lmao
class Track:
    title: str
    artist: str
    _service_metadata: dict[str, Any]

    def __init__(
        self, title: str, artist: str, *, service: str | None = None, metadata: Any = None
    ):
        self.title = title
        self.artist = artist
        self._service_metadata = {}

        if service is not None:
            self._service_metadata[service] = metadata

    def add_metadata(self, service: str, metadata: Any):
        self._service_metadata[service] = metadata

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Track):
            return False

        if self.title != other.title or self.artist != other.artist:
            return False

        return True

    def __repr__(self) -> str:
        return f'Track(title={self.title!r}, artist={self.artist!r})'

    def __str__(self) -> str:
        return f'{self.title} by {self.artist}' if self.artist else self.title


    def __hash__(self) -> int:
        return hash((self.title, self.artist))
