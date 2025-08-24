from torrent_companion.scrappers.models import BaseTorrentData, BaseUploaderProfile

PLATAFORM_NAME = "ThePirateBay"


class PBUploaderProfile(BaseUploaderProfile):
    plataform: str = PLATAFORM_NAME


class PBTorrentData(BaseTorrentData):
    source: str = PLATAFORM_NAME
    pb_id: str
    pb_category: int
    pb_status: str
    imdb_id: str
