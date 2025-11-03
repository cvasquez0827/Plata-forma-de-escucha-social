"""Keyword driven topic detection."""

from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, Mapping, Sequence

from ..models import AnalyzedPost


class TopicClassifier:
    """Assigns topics to posts based on keyword dictionaries."""

    def __init__(self, topic_keywords: Mapping[str, Sequence[str]]):
        self.topic_keywords = {
            topic: {keyword.lower() for keyword in keywords}
            for topic, keywords in topic_keywords.items()
        }

    def classify(self, post: AnalyzedPost) -> AnalyzedPost:
        text_lower = post.text.lower()
        matched_topics = [
            topic
            for topic, keywords in self.topic_keywords.items()
            if any(keyword in text_lower for keyword in keywords)
        ]
        post.topics = matched_topics
        return post

    def summarize(self, posts: Iterable[AnalyzedPost]) -> Dict[str, int]:
        counter: Counter[str] = Counter()
        for post in posts:
            for topic in post.topics:
                counter[topic] += 1
        return dict(counter)


__all__ = ["TopicClassifier"]
