from enum import Enum


class IndexerType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class IndexerGenre(Enum):
    MOVIES = "movies"
    ANIME = "anime"
    GAMES = "games"
    TV_SHOWS = "tv_shows"


class IndexerHealth(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ScrapperType(Enum):
    STATIC = "static"
    BROWSER = "browser"
    API = "api"
