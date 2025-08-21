from torrent_companion.indexers.base_indexer import BaseIndexer
from torrent_companion.indexers.common_types import IndexerGenre, IndexerType
from torrent_companion.indexers.definitions.piratebay.scrapper import PirateBayScrapper


class PirateBayIndexer(BaseIndexer):
    def __init__(self, _job_timer_override: int = 10):
        super().__init__(
            name="The Pirate Bay",
            description="A popular torrent indexer known for its vast collection of torrents.",
            idxtype=IndexerType.PUBLIC,
            language="en",
            genres=(IndexerGenre.MOVIES, IndexerGenre.TV_SHOWS, IndexerGenre.GAMES),
            scrapper=PirateBayScrapper(),
            _job_timer_override=_job_timer_override,
        )

    async def get_best_movie_torrent(
        self,
        analyze_torrent: bool = True, # Whether to analyze the torrent for quality (e.g., resolution, codec)
        analyze_files: bool = False, # Resource intensive
        analyze_uploader: bool = False, # Resource intensive (requires additional requests)
    ):
        """Get the best movie torrent available."""
        pass
