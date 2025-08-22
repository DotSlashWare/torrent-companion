from pydantic import BaseModel


class BaseUploaderProfile(BaseModel):
    """Base model for uploader profile (used for analysis)."""
    name: str
    rating: float = 0.0
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
    size: int  # in bytes
    leechers: int
    seeders: int
    info_hash: str
    magnet_link: str
    added_date: str  # should be in iso format


class BaseTorrentSearchResponse(BaseModel):
    """Base model for torrent search response."""

    success: bool
    query: str
    results: list[BaseTorrentData]
    total_results: int
