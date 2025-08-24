import httpx
import logging
from typing import List
from datetime import datetime

from torrent_companion.enums import MediaType
from torrent_companion.scrappers.base_scrapper import BaseScrapper
from torrent_companion.scrappers.enums import ScrapperType

logger = logging.getLogger(__name__)

class PirateBayScrapper(BaseScrapper):
    def __init__(self, base_url: str):
        super().__init__(
            service_name="ThePirateBay",
            base_url=base_url,
            requires_auth=False,
            media_support={MediaType.MOVIE, MediaType.TV_SHOW},
            scrapper_type=ScrapperType.REQUESTS,
        )
        
        self.request_client = httpx.AsyncClient()
        self.build_template_urls()
        
    def build_template_urls(self) -> None:
        """Build the URLs used by the scrapper."""
        self.search_url = f"{self.base_url}/q.php?q={{query}}&cat={{category}}"

        self.torrent_info = f"{self.base_url}/t.php?id={{id}}"
        self.file_info_url = f"{self.base_url}/f.php?id={{id}}"
        self.magnet_url = f"magnet:?xt=urn:btih:{{hash}}"

        self.uploader_pages_url = f"{self.base_url}/q.php?q=pcnt:{{username}}"
        self.uploader_profile_url = f"{self.base_url}/q.php?q=user:{{username}}"

    async def update_health(self) -> None:
        """Update the health status of the scrapper."""
        try:
            response = await self.request_client.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.is_healthy = True
                logger.info(f"{self.service_name} is healthy.")
            else:
                self.is_healthy = False
                logger.warning(f"{self.service_name} returned status code {response.status_code}.")
        except httpx.RequestError as e:
            self.is_healthy = False
            logger.error(f"Health check for {self.service_name} failed: {e}")
