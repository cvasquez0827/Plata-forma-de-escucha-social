"""Pipeline orchestrating ingestion and analysis."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping

from .analysis import aggregations, sentiment, topics
from .ingestion.base import PipelineConfigError, SocialSource
from .ingestion.json_file import JSONFileSource
from .models import AnalyzedPost


SOURCE_REGISTRY: Dict[str, type[SocialSource]] = {
    "json_file": JSONFileSource,
}


@dataclass(slots=True)
class PipelineConfig:
    sources: List[SocialSource]
    topic_classifier: topics.TopicClassifier

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "PipelineConfig":
        try:
            source_configs = payload["sources"]
            topic_config = payload.get("topics", {})
        except KeyError as exc:
            raise PipelineConfigError(f"Missing configuration key: {exc}") from exc

        if not isinstance(source_configs, list):
            raise PipelineConfigError("'sources' must be a list")

        sources: List[SocialSource] = []
        for source_payload in source_configs:
            if not isinstance(source_payload, Mapping):
                raise PipelineConfigError("Source configuration must be a mapping")
            try:
                source_type = source_payload["type"]
            except KeyError as exc:
                raise PipelineConfigError("Source configuration missing 'type'") from exc

            if source_type not in SOURCE_REGISTRY:
                raise PipelineConfigError(f"Unsupported source type: {source_type}")

            source_cls = SOURCE_REGISTRY[source_type]
            kwargs = {
                key: value
                for key, value in source_payload.items()
                if key != "type"
            }
            sources.append(source_cls(**kwargs))  # type: ignore[arg-type]

        topic_keywords = (
            topic_config.get("keywords") if isinstance(topic_config, Mapping) else {}
        )
        if not isinstance(topic_keywords, Mapping):
            raise PipelineConfigError("topics.keywords must be a mapping")

        classifier = topics.TopicClassifier(topic_keywords)
        return cls(sources=sources, topic_classifier=classifier)

    @classmethod
    def from_file(cls, path: str | Path) -> "PipelineConfig":
        path = Path(path)
        with path.open("r", encoding="utf8") as handle:
            data = json.load(handle)
        if not isinstance(data, Mapping):
            raise PipelineConfigError("Configuration must be a JSON object")
        return cls.from_dict(data)


def run_pipeline(config: PipelineConfig, *, limit_per_source: int | None = None) -> Dict[str, object]:
    analyzed_posts: List[AnalyzedPost] = []

    for source in config.sources:
        for post in source.fetch(limit=limit_per_source):
            enriched = sentiment.analyze_post(post)
            config.topic_classifier.classify(enriched)
            analyzed_posts.append(enriched)

    insights = build_insights(analyzed_posts)

    return {
        "posts": analyzed_posts,
        "insights": insights,
    }


def build_insights(posts: List[AnalyzedPost]) -> Dict[str, object]:
    sentiment_summary = aggregations.sentiment_distribution(posts)
    volume_by_country = aggregations.volume_by_country(posts)
    timeline = aggregations.timeline_volume(posts)

    return {
        "sentiment": sentiment_summary,
        "countries": volume_by_country,
        "timeline": timeline,
        "sample_posts": [post.post_id for post in posts[:5]],
    }


__all__ = [
    "PipelineConfig",
    "build_insights",
    "run_pipeline",
]
