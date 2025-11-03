"""Lightweight sentiment analysis using lexicon heuristics."""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping

from ..models import AnalyzedPost, Post

POSITIVE_TERMS = {
    "excelente",
    "bueno",
    "genial",
    "feliz",
    "satisfecho",
    "mejor",
    "fantástico",
    "increíble",
    "gracias",
    "love",
    "great",
    "amazing",
}
NEGATIVE_TERMS = {
    "malo",
    "terrible",
    "horrible",
    "triste",
    "pésimo",
    "odio",
    "reclamo",
    "demora",
    "tarde",
    "fraude",
    "scam",
    "bad",
    "awful",
}
TOKEN_RE = re.compile(r"[\wáéíóúñü]+", re.UNICODE)


@dataclass(slots=True)
class SentimentResult:
    score: float
    label: str
    contributing_tokens: Mapping[str, int]


def analyze_post(post: Post) -> AnalyzedPost:
    tokens = [t.lower() for t in TOKEN_RE.findall(post.text)]
    pos = sum(1 for token in tokens if token in POSITIVE_TERMS)
    neg = sum(1 for token in tokens if token in NEGATIVE_TERMS)
    total = len(tokens) or 1

    score = (pos - neg) / math.sqrt(total)
    if score > 0.25:
        label = "positive"
    elif score < -0.25:
        label = "negative"
    else:
        label = "neutral"

    contributing = {}
    for token in tokens:
        if token in POSITIVE_TERMS or token in NEGATIVE_TERMS:
            contributing[token] = contributing.get(token, 0) + 1

    base = asdict(post)
    return AnalyzedPost(
        **base,  # type: ignore[arg-type]
        sentiment_score=score,
        sentiment_label=label,
        topics=[],
        entities=[],
        flags={"sentiment_tokens": contributing},
    )


def analyze_posts(posts: Iterable[Post]) -> Iterable[AnalyzedPost]:
    for post in posts:
        yield analyze_post(post)


__all__ = ["SentimentResult", "analyze_post", "analyze_posts"]
