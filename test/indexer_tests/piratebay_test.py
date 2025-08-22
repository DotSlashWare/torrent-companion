import pytest
import pytest_asyncio
from torrent_companion.indexers.definitions.piratebay.scrapper import PirateBayScrapper
from torrent_companion.indexers.definitions.piratebay.indexer import PirateBayIndexer
from torrent_companion.indexers.common_types import IndexerGenre, IndexerHealth, IndexerType
from torrent_companion.indexers.definitions.piratebay.types import PirateBayCategory

def test_piratebay_scrapper_initialization():
    s = PirateBayScrapper()

    assert s.base_url == "https://apibay.org"

    assert s.search_url == "https://apibay.org/q.php?q={query}"
    assert s.torrent_info == "https://apibay.org/t.php?id={id}"
    assert s.file_info_url == "https://apibay.org/f.php?id={id}"
    assert s.magnet_url == "magnet:?xt=urn:btih:{hash}"

def test_piratebay_indexer_initialization():
    indexer = PirateBayIndexer()

    assert indexer.name == "The Pirate Bay"
    assert indexer.description == "A popular torrent indexer known for its vast collection of torrents."
    assert indexer.type == IndexerType.PUBLIC
    assert indexer.language == "en"
    assert IndexerGenre.MOVIES in indexer.genres
    assert IndexerGenre.TV_SHOWS in indexer.genres
    assert IndexerGenre.GAMES in indexer.genres
    
def test_health_check_job_initialization():
    indexer = PirateBayIndexer()

    assert indexer._job is not None
    assert indexer._job.name == "health_check"
    assert indexer._job.next_run_time is not None
    assert indexer._job.id == f"indexer-health-{indexer.name}"

@pytest.mark.asyncio
async def test_health_check_piratebay_indexer():
    indexer = PirateBayIndexer()

    assert indexer.health == IndexerHealth.UNKNOWN

    await indexer.update_health()
    assert indexer.health == IndexerHealth.HEALTHY or indexer.health == IndexerHealth.UNHEALTHY
    
@pytest.mark.asyncio
async def test_search_piratebay():
    scrapper = PirateBayScrapper()
    
    response = await scrapper.search("matrix", category=None)
    
    assert response.success is True
    assert len(response.results) > 0
    assert response.category == PirateBayCategory.ALL
    
    for result in response.results:
        assert result.id is not None
        assert result.uploader is not None
        assert result.status is not None
        assert isinstance(result.category, int)
        
@pytest.mark.asyncio
async def test_get_torrent_info_piratebay():
    scrapper = PirateBayScrapper()

    torrent_id = "7349687"
    torrent_info = await scrapper.get_torrent_info(torrent_id)
    
    assert torrent_info is not None
    assert torrent_info.id == torrent_id
    assert torrent_info.name == "The Matrix (1999) 1080p BrRip x264 - 1.85GB - YIFY"
    assert torrent_info.info_hash == "D7A46713EAEE18C746B3254B7D1492A50FD9D6CE"
    assert torrent_info.leechers >= 0
    assert torrent_info.seeders >= 0
    assert torrent_info.size > 0
    assert torrent_info.uploader == "YIFY"
    assert isinstance(torrent_info.category, int)
    assert torrent_info.status == "vip"
    assert torrent_info.description is not None
