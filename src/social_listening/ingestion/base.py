"""Ingestion interfaces for social listening sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from ..models import Post


class SocialSource(ABC):
    """Abstract base class for social listening data sources."""

    @abstractmethod
    def fetch(self, *, limit: int | None = None) -> Iterable[Post]:
        """Yield normalized :class:`Post` objects from the underlying source."""


class PipelineConfigError(RuntimeError):
    """Raised when a pipeline configuration is invalid."""


__all__ = ["SocialSource", "PipelineConfigError"]
