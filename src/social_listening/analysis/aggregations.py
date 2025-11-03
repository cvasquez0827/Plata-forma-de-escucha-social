"""Aggregation utilities for summarising analyzed posts."""

from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable

from ..models import AnalyzedPost


def sentiment_distribution(posts: Iterable[AnalyzedPost]) -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for post in posts:
        counter[post.sentiment_label] += 1
    return dict(counter)


def volume_by_country(posts: Iterable[AnalyzedPost]) -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for post in posts:
        country = post.country or "UNK"
        counter[country] += 1
    return dict(counter)


def timeline_volume(posts: Iterable[AnalyzedPost], *, granularity: str = "day") -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for post in posts:
        timestamp = post.timestamp
        if granularity == "hour":
            key = timestamp.strftime("%Y-%m-%dT%H:00")
        else:
            key = timestamp.strftime("%Y-%m-%d")
        counter[key] += 1
    return dict(counter)


__all__ = ["sentiment_distribution", "volume_by_country", "timeline_volume"]
