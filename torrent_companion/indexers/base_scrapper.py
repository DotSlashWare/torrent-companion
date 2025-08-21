from typing import Tuple

import httpx
from .common_types import ScrapperType


class BaseScrapper:
    def __init__(
        self,
        base_url: str,
        is_authenticated: bool,
        scrapper_type: Tuple[ScrapperType],
    ):
        self.base_url = base_url
        self.scrapper_type = scrapper_type

        if is_authenticated:
            self.authenticate()

    @staticmethod
    def build_url(template: str, **kwargs) -> str:
        """Build a URL from a template and keyword arguments."""
        return template.format(**kwargs)

    def authenticate(self) -> None:
        """Authenticate with the indexer if required."""
        raise NotImplementedError("Subclasses should implement this method.")

    def test_connection(self) -> bool:
        """Test the connection to the indexer."""
        response = httpx.get(self.base_url)
        return response.status_code == 200

    async def aync_test_connection(self) -> bool:
        """Test the connection to the indexer."""
        raise NotImplementedError("Subclasses should implement this method.")
