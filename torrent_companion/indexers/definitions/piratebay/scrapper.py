from datetime import datetime
from typing import List
import httpx
import logging
from torrent_companion.indexers.common_types import ScrapperType
from torrent_companion.indexers.base_scrapper import BaseScrapper
from torrent_companion.indexers.definitions.piratebay.types import PirateBayCategory
from torrent_companion.indexers.definitions.piratebay.models import (
    DetailedPBTorrentData, 
    PBTorrentData,
    PBTorrentSearchResponse,
    PBUploaderProfile,
)

logger = logging.getLogger(__name__)


class PirateBayScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(
            base_url="https://apibay.org",
            is_authenticated=False,
            scrapper_type=(ScrapperType.API),
        )

        self.request_client = httpx.AsyncClient()
        self.build_template_urls()

    async def aync_test_connection(self) -> bool:
        """Test the connection to the indexer."""
        response = await self.request_client.get(self.base_url)
        return response.status_code == 200

    def build_template_urls(self) -> None:
        """Build the URLs used by the scrapper."""
        self.search_url = f"{self.base_url}/q.php?q={{query}}&cat={{category}}"

        self.torrent_info = f"{self.base_url}/t.php?id={{id}}"
        self.file_info_url = f"{self.base_url}/f.php?id={{id}}"
        self.magnet_url = f"magnet:?xt=urn:btih:{{hash}}"

        self.uploader_pages_url = f"{self.base_url}/q.php?q=pcnt:{{username}}"
        self.uploader_profile_url = f"{self.base_url}/q.php?q=user:{{username}}"

    async def search(
        self, query: str, category: PirateBayCategory = PirateBayCategory.ALL
    ) -> PBTorrentSearchResponse:
        """Search for torrents using the provided query and category."""
        category = PirateBayCategory.ALL if category is None else category
        url = self.build_url(self.search_url, query=query, category=category)
        response = await self.request_client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch search results for {query} from Pirate Bay")
            return PBTorrentSearchResponse(
                success=False,
                query=query,
                results=[],
                total_results=0,
                category=category,
            )

        data = response.json()
        results = [
            PBTorrentData(
                id=str(item["id"]),
                name=item["name"],
                info_hash=item["info_hash"],
                leechers=item["leechers"],
                seeders=item["seeders"],
                size=item["size"],
                uploader=item["username"],
                added_date=datetime.fromtimestamp(int(item["added"])).isoformat(),
                status=item.get("status", "unknown"),
                category=item.get("category", PirateBayCategory.ALL.value),
                imdb=item.get("imdb", ""),
                magnet_link=self.build_url(self.magnet_url, hash=item["info_hash"]),
            )
            for item in list(data)
        ]

        return PBTorrentSearchResponse(
            success=True,
            query=query,
            results=results,
            total_results=len(results),
            category=category,
        )

    async def get_torrent_info(self, torrent_id: str) -> DetailedPBTorrentData:
        """Get detailed information about a torrent by its ID."""
        url = self.build_url(self.torrent_info, id=torrent_id)
        response = await self.request_client.get(url)

        if response.status_code != 200:
            logger.error(
                f"Failed to fetch torrent info for ID {torrent_id} from Pirate Bay"
            )
            return None

        data = response.json()
        return DetailedPBTorrentData(
            id=str(data["id"]),
            name=data["name"],
            info_hash=data["info_hash"],
            leechers=data["leechers"],
            seeders=data["seeders"],
            size=data["size"],
            uploader=data["username"],
            added_date=datetime.fromtimestamp(int(data["added"])).isoformat(),
            status=data.get("status", "unknown"),
            category=data.get("category", PirateBayCategory.ALL.value),
            imdb=data.get("imdb", ""),
            num_files=data.get("num_files", 0),
            description=data.get("description", ""),
            language=data.get("language", 0),
            textlanguage=data.get("textlanguage", 0),
            magnet_link=self.build_url(self.magnet_url, hash=data["info_hash"]),
        )

    async def get_uploader_profile(
        self, username: str, read_pages: int = 5
    ) -> PBUploaderProfile:
        """Get profile information about an uploader by their username. Used for analysis."""
        url = self.build_url(self.uploader_pages_url, username=username)
        response = await self.request_client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch uploader profile for {username}")
            return None

        max_pages = int(response.text)
        read_pages = min(read_pages, max_pages)

        torrents_data = []
        for page in range(read_pages):
            url = self.build_url(
                self.uploader_profile_url, username=f"{username}:{page}"
            )
            response = await self.request_client.get(url)

            if response.status_code != 200:
                logger.error(
                    f"Failed to fetch uploader profile for {username} on page {page}"
                )
                continue

            data = response.json()

            for item in data:
                torrents_data.append(
                    PBTorrentData(
                        id=str(item["id"]),
                        name=item["name"],
                        info_hash=item["info_hash"],
                        leechers=item["leechers"],
                        seeders=item["seeders"],
                        size=item["size"],
                        uploader=item["username"],
                        added_date=datetime.fromtimestamp(
                            int(item["added"])
                        ).isoformat(),
                        status=item.get("status", "unknown"),
                        category=item.get("category", PirateBayCategory.ALL.value),
                        imdb=item.get("imdb", ""),
                    )
                )

        if not torrents_data:
            logger.warning(f"No torrents found for uploader {username}")
            return None

        url = self.build_url(
            self.uploader_profile_url, username=f"{username}:{max_pages}"
        )
        response = await self.request_client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch uploader's last profile page for {username}")
            return None

        last_page_data = response.json()
        oldest_activity = datetime.fromtimestamp(
            int(last_page_data[0]["added"])
        ).isoformat()

        total_seeders = sum(torrent.seeders for torrent in torrents_data)
        total_leechers = sum(torrent.leechers for torrent in torrents_data)
        average_uploads_per_month = len(torrents_data) / (read_pages or 1)
        average_seeders_per_upload = total_seeders / (len(torrents_data) or 1)
        average_leechers_per_upload = total_leechers / (len(torrents_data) or 1)
        recent_activity = max(torrent.added_date for torrent in torrents_data)
        fetched_at = datetime.now().isoformat()

        return PBUploaderProfile(
            name=username,
            total_pages=read_pages,
            total_seeders=total_seeders,
            total_leechers=total_leechers,
            average_uploads_per_month=average_uploads_per_month,
            average_seeders_per_upload=average_seeders_per_upload,
            average_leechers_per_upload=average_leechers_per_upload,
            recent_activity=recent_activity,
            oldest_activity=oldest_activity,
            fetched_at=fetched_at,
        )
