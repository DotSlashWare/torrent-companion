import httpx
from torrent_companion.indexers.common_types import ScrapperType
from torrent_companion.indexers.base_scrapper import BaseScrapper


class PirateBayScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(
            base_url="https://apibay.org",
            is_authenticated=False,
            scrapper_type=(ScrapperType.API),
        )

        self.request_client = httpx.AsyncClient()
        if not self.test_connection():
            raise ConnectionError("Failed to connect to Pirate Bay API")

        self.build_template_urls()

    def build_template_urls(self) -> None:
        """Build the URLs used by the scrapper."""
        self.search_url = f"{self.base_url}/q.php?q={{query}}"
        self.torrent_info = f"{self.base_url}/t.php?id={{id}}"
        self.file_info_url = f"{self.base_url}/f.php?id={{id}}"
        self.magnet_url = f"magnet:?xt=urn:btih:{{hash}}"

    def test_connection(self) -> bool:
        """Override to implement specific connection testing logic for Pirate Bay."""
        return self.request_client.get(self.base_url).status_code == 200
