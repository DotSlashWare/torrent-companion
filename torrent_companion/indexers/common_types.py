from enum import Enum


class IndexerType(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class IndexerGenre(Enum):
    MOVIES = "MOVIES"
    ANIME = "ANIME"
    GAMES = "GAMES"
    TV_SHOWS = "TV_SHOWS"


class IndexerHealth(Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class ScrapperType(Enum):
    STATIC = "STATIC"
    BROWSER = "BROWSER"
    API = "API"
