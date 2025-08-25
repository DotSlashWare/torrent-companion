from torrent_companion.scrappers.models import BaseTorrentData, BaseTorrentSearchResponse, BaseUploaderProfile

PLATAFORM_NAME = "ThePirateBay"


class UploaderProfile(BaseUploaderProfile):
    plataform: str = PLATAFORM_NAME


class TorrentData(BaseTorrentData):
    source: str = PLATAFORM_NAME
    pb_id: str
    pb_category: int
    pb_status: str
    imdb_id: str
    
class TorrentSearchResponse(BaseTorrentSearchResponse):
    results: list[TorrentData]