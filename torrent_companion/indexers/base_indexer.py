import time
import logging
from typing import Tuple
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .base_scrapper import BaseScrapper
from .common_types import IndexerGenre, IndexerType, IndexerHealth

logger = logging.getLogger(__name__)


class BaseIndexer:
    def __init__(
        self,
        name: str,
        description: str,
        idxtype: IndexerType,
        language: str,
        genres: Tuple[IndexerGenre],
        scrapper: BaseScrapper,
        _job_timer_override: int = 10,
    ):
        self.name = name
        self.description = description
        self.type = idxtype
        self.language = language
        self.genres = genres

        self.scrapper = scrapper
        self.last_updated = None
        self.health = IndexerHealth.UNKNOWN

        self._scheduler = AsyncIOScheduler()
        self._job = self._scheduler.add_job(
            self.update_health,
            name="health_check",
            trigger="interval",
            minutes=_job_timer_override,
            next_run_time=datetime.now(),
            id=f"indexer-health-{self.name}",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

    def __del__(self):
        if hasattr(self, "_job") and self._job:
            self._job.remove()
        logger.debug(f"Indexer {self.name} deleted")

    async def update_health(self) -> None:
        """Update the health status of the indexer by testing the connection."""
        logger.debug(f"Checking health of {self.name} indexer")
        if not await self.scrapper.aync_test_connection():
            logger.warning(f"{self.name} indexer failed the healthcheck")
            self.health = IndexerHealth.UNHEALTHY
            self.last_updated = time.time()
        else:
            logger.info(f"{self.name} indexer passed the healthcheck")
            self.health = IndexerHealth.HEALTHY
            self.last_updated = time.time()
