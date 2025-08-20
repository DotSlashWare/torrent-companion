import pytest
from torrent_companion.indexers.definitions.piratebay.scrapper import PirateBayScrapper
from torrent_companion.indexers.definitions.piratebay.indexer import PirateBayIndexer
from torrent_companion.indexers.common_types import IndexerType, IndexerGenre


class _FakeResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


class _FakeClientOK:
    def get(self, url):
        return _FakeResponse(200)

    def __aenter__(self):  # in case context mgmt is used later
        return self

    def __aexit__(self, *args):
        pass


class _FakeClientFail:
    def get(self, url):
        return _FakeResponse(500)


def test_piratebay_scrapper_initialization_success(monkeypatch):
    # Patch httpx.AsyncClient used inside the scrapper module
    import torrent_companion.indexers.definitions.piratebay.scrapper as scr_mod

    monkeypatch.setattr(scr_mod.httpx, "AsyncClient", lambda: _FakeClientOK())

    s = PirateBayScrapper()

    assert s.base_url == "https://apibay.org"
    # URL templates built
    assert s.search_url == "https://apibay.org/q.php?q={query}"
    assert s.torrent_info == "https://apibay.org/t.php?id={id}"
    assert s.file_info_url == "https://apibay.org/f.php?id={id}"
    assert s.magnet_url == "magnet:?xt=urn:btih:{hash}"
    # test_connection should work
    assert s.test_connection() is True


def test_piratebay_scrapper_initialization_failure(monkeypatch):
    import torrent_companion.indexers.definitions.piratebay.scrapper as scr_mod

    monkeypatch.setattr(scr_mod.httpx, "AsyncClient", lambda: _FakeClientFail())

    with pytest.raises(ConnectionError):
        PirateBayScrapper()


def test_piratebay_scrapper_test_connection_called(monkeypatch):
    calls = {"count": 0}

    original = PirateBayScrapper.test_connection

    def wrapped(self):
        calls["count"] += 1
        return True

    monkeypatch.setattr(PirateBayScrapper, "test_connection", wrapped)

    # Need a fake client so __init__ does not touch network
    import torrent_companion.indexers.definitions.piratebay.scrapper as scr_mod

    monkeypatch.setattr(scr_mod.httpx, "AsyncClient", lambda: _FakeClientOK())

    PirateBayScrapper()
    assert calls["count"] == 1

    # restore (not strictly necessary, but clean)
    monkeypatch.setattr(PirateBayScrapper, "test_connection", original)


def test_piratebay_indexer_attributes():
    idx = PirateBayIndexer()
    assert idx.name == "The Pirate Bay"
    assert "torrent" in idx.description.lower()
    assert idx.idxtype == IndexerType.PUBLIC
    assert idx.language == "en"
    assert IndexerGenre.MOVIES in idx.genres
    assert IndexerGenre.TV_SHOWS in idx.genres
    assert IndexerGenre.GAMES in idx.genres
    # Scrapper class reference
    assert getattr(idx, "scrapper") == PirateBayScrapper
