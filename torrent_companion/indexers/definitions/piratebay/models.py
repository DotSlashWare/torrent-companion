from pydantic import BaseModel

from torrent_companion.indexers.common_models import (
    BaseTorrentData,
    BaseTorrentSearchResponse,
    BaseUploaderProfile,
)
from torrent_companion.indexers.definitions.piratebay.types import PirateBayCategory


class PBUploaderProfile(BaseUploaderProfile):
    plataform: str = "Pirate Bay"


class DetailedPBTorrentData(BaseTorrentData):
    """Detailed model for Pirate Bay torrent data."""

    id: str
    category: int  # should convert to PirateBayCategory if possible
    status: str
    num_files: int
    description: str
    imdb: str
    language: int
    textlanguage: int


class PBTorrentData(BaseTorrentData):
    """Model for Pirate Bay torrent data."""

    id: str
    source: str = "PirateBay"
    category: int  # should convert to PirateBayCategory if possible
    status: str
    imdb: str


class PBTorrentSearchResponse(BaseTorrentSearchResponse):
    """Model for Pirate Bay torrent search response."""

    category: PirateBayCategory = PirateBayCategory.ALL
