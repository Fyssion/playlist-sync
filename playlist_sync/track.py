# SPDX-FileCopyrightText: 2024-present Fyssion <fyssioncodes@gmail.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any


# I should've used a dataclass lmao
class Track:
    title: str
    artist: str

    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

        def __eq__(self, other: Any) -> bool:
            if not isinstance(other, Track):
                return False

            if self.title != other.title or self.artist != other.artist:
                return False

            return True

    def __repr__(self) -> str:
        return f'Track(title={self.title!r}, artist={self.artist!r})'
