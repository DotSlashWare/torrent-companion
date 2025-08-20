import time
import schedule
import logging
from typing import Tuple

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

        self._job = schedule.every(_job_timer_override).minutes.do(self.update_health)

        self.update_health()

    def __del__(self):
        if self._job:
            schedule.cancel_job(self._job)
            self._job = None
        logger.debug(f"Indexer {self.name} deleted")

    def update_health(self) -> None:
        """Update the health status of the indexer by testing the connection."""
        logger.debug(f"Checking health of {self.name} indexer")
        if not self.scrapper.test_connection():
            logger.warning(f"{self.name} indexer failed the healthcheck")
            self.health = IndexerHealth.UNHEALTHY
            self.last_updated = time.time()
        else:
            logger.info(f"{self.name} indexer passed the healthcheck")
            self.health = IndexerHealth.HEALTHY
            self.last_updated = time.time()

    @property
    def get_health(self) -> IndexerHealth:
        """Get the current health status of the indexer."""
        return self.health
