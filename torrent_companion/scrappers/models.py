from typing import Literal
from pydantic import BaseModel

from torrent_companion.enums import MediaType


class BaseUploaderProfile(BaseModel):
    """Base model for uploader profile (used for analysis)."""

    name: str
    plataform: str

    total_pages: int
    total_seeders: int
    total_leechers: int

    average_uploads_per_month: float
    average_seeders_per_upload: float
    average_seeders_per_upload: float

    recent_activity: str  # should be in iso format
    oldest_activity: str  # should be in iso format

    fetched_at: str  # should be in iso format


class BaseTorrentData(BaseModel):
    """Base model for torrent data."""

    name: str
    uploader: str
    leechers: int  # only used in analysis (not to be saved)
    seeders: int  # only used in analysis (not to be saved)
    added_date: str  # should be in iso format

    size: int  # in bytes
    media_type: MediaType  # movie or tv_show
    quality: str = "Unknown"  # e.g., 1080p, 720p
    language: str = "Unknown"  # e.g., English, Spanish
    episode_number: int | None = None  # for TV shows
    season_number: int | None = None  # for TV shows

    source: str = "Unknown"  # e.g., PirateBay, 1337x
    info_hash: str  # torrent info hash
    magnet_link: str  # magnet link (based on info hash)


class BaseTorrentSearchResponse(BaseModel):
    """Base model for torrent search response."""

    success: bool
    query: str
    results: list[BaseTorrentData]
    total_results: int
    error: str | None = None
