from typing import Tuple
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

    def build_url(template: str, **kwargs) -> str:
        return template.format(**kwargs)

    def test_connection(self) -> bool:
        """Test the connection to the indexer."""
        return True

    def authenticate(self) -> None:
        """Authenticate with the indexer if required."""
        pass
