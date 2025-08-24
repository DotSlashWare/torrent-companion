from enum import Enum

class IndexerAvailability(Enum):
    UNKNOWN = "unknown"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    PARTIALLY_AVAILABLE = "partially_available"