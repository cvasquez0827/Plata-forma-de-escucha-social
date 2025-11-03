"""Core domain models for the social listening pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(slots=True)
class Post:
    """Normalized representation of a social media or media post."""

    post_id: str
    source: str
    author_id: str
    author: Optional[str]
    text: str
    timestamp: datetime
    url: Optional[str] = None
    lang: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AnalyzedPost(Post):
    """Post enriched with NLP analysis signals."""

    sentiment_score: float = 0.0
    sentiment_label: str = "neutral"
    topics: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    flags: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Insight:
    """Aggregate insight generated from a set of posts."""

    title: str
    summary: str
    posts: Iterable[AnalyzedPost]
    metrics: Dict[str, Any]
