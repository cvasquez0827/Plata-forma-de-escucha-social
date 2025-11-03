"""Local JSON ingestion source for prototyping and offline testing."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Mapping

from .base import SocialSource
from ..models import Post


class JSONFileSource(SocialSource):
    """Loads posts from a JSON file containing a list of dictionaries."""

    def __init__(self, path: str | Path, *, default_source: str = "json") -> None:
        self.path = Path(path)
        self.default_source = default_source

    def _load(self) -> List[Mapping[str, object]]:
        with self.path.open("r", encoding="utf8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("JSON payload must be a list of objects")
        return data  # type: ignore[return-value]

    def fetch(self, *, limit: int | None = None) -> Iterable[Post]:
        rows = self._load()
        if limit is not None:
            rows = rows[:limit]

        for row in rows:
            timestamp = row.get("timestamp")
            if isinstance(timestamp, str):
                timestamp_dt = datetime.fromisoformat(timestamp)
            elif isinstance(timestamp, (int, float)):
                timestamp_dt = datetime.fromtimestamp(timestamp)
            else:
                timestamp_dt = datetime.utcnow()

            yield Post(
                post_id=str(row.get("post_id") or row.get("id") or ""),
                source=str(row.get("source") or self.default_source),
                author_id=str(row.get("author_id") or row.get("author") or "anon"),
                author=str(row.get("author_name") or row.get("author")),
                text=str(row.get("text") or row.get("content") or ""),
                timestamp=timestamp_dt,
                url=row.get("url") and str(row["url"]),
                lang=row.get("lang") and str(row["lang"]),
                country=row.get("country") and str(row["country"]),
                city=row.get("city") and str(row["city"]),
                metadata={k: v for k, v in row.items() if k not in {
                    "post_id",
                    "id",
                    "source",
                    "author_id",
                    "author",
                    "author_name",
                    "text",
                    "content",
                    "timestamp",
                    "url",
                    "lang",
                    "country",
                    "city",
                }},
            )
