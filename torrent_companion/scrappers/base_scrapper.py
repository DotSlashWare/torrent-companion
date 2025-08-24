import functools
import inspect
import time
from typing import Tuple
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from torrent_companion.enums import MediaType
from torrent_companion.scrappers.enums import ScrapperType


class BaseScrapper:
    _TIMING_EXCLUDE: set[str] = {
        "__init__",
        "_record_duration",
        "_wrap_timed",
        "authenticate",
        "update_health",
        "build_url",
    }

    def __init_subclass__(cls, **kwargs):
        """Auto-wrap all public instance methods in subclasses to time them."""
        super().__init_subclass__(**kwargs)

        for name, attr in list(cls.__dict__.items()):
            # Only wrap plain functions that become instance methods
            if not inspect.isfunction(attr):
                continue
            if name.startswith("_") or name in BaseScrapper._TIMING_EXCLUDE:
                continue
            if getattr(attr, "_timed_wrapped", False):
                continue

            setattr(cls, name, cls._wrap_timed(attr))

    @staticmethod
    def _wrap_timed(func):
        """Create a wrapper that measures duration and updates instance average."""
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(self, *args, **kwargs):
                t0 = time.perf_counter()
                try:
                    return await func(self, *args, **kwargs)
                finally:
                    self._record_duration(time.perf_counter() - t0)

            async_wrapper._timed_wrapped = True  # type: ignore[attr-defined]
            return async_wrapper

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            t0 = time.perf_counter()
            try:
                return func(self, *args, **kwargs)
            finally:
                self._record_duration(time.perf_counter() - t0)

        wrapper._timed_wrapped = True  # type: ignore[attr-defined]
        return wrapper

    def __init__(
        self,
        service_name: str,
        base_url: str,
        requires_auth: bool,
        media_support: Tuple[MediaType],
        scrapper_type: ScrapperType,
        _job_timer_override: int = 10,
    ):
        self.service_name = service_name
        self.base_url = base_url
        self.media_support = media_support
        self.scrapper_type = scrapper_type

        self.is_healthy = False
        self.update_health()

        self.avrg_response_time = 0.0
        self._rt_count = 0

        if requires_auth:
            self.authenticate()

        self._scheduler = AsyncIOScheduler()
        self._job = self._scheduler.add_job(
            self.update_health,
            name="health_check",
            trigger="interval",
            minutes=_job_timer_override,
            next_run_time=datetime.now(),
            id=f"indexer-health-{self.service_name.lower()}",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        self._scheduler.start()

    def _record_duration(self, seconds: float) -> None:
        """Incremental average: O(1) memory, stable for long runs."""
        self._rt_count += 1
        self.avrg_response_time += (seconds - self.avrg_response_time) / self._rt_count

    @staticmethod
    def build_url(template: str, **kwargs) -> str:
        """Build a URL from a template and keyword arguments."""
        return template.format(**kwargs)

    def authenticate(self) -> None:
        """Authenticate with the indexer if required."""
        raise NotImplementedError("Subclasses should implement this method.")

    async def update_health(self) -> None:
        """Update the health status of the scrapper."""
        raise NotImplementedError("Subclasses should implement this method.")
