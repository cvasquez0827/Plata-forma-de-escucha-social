"""Command line interface for running the social listening pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .pipeline import PipelineConfig, run_pipeline


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run social listening analysis")
    parser.add_argument(
        "config",
        type=Path,
        help="Path to pipeline configuration JSON file.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit of posts to process per source.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the aggregated insights as JSON.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = PipelineConfig.from_file(args.config)

    result = run_pipeline(config, limit_per_source=args.limit)
    output_data: dict[str, Any] = {
        "insights": result["insights"],
        "posts": [
            {
                "post_id": post.post_id,
                "source": post.source,
                "author_id": post.author_id,
                "text": post.text,
                "sentiment": post.sentiment_label,
                "sentiment_score": round(post.sentiment_score, 3),
                "topics": post.topics,
                "country": post.country,
                "timestamp": post.timestamp.isoformat(),
            }
            for post in result["posts"]
        ],
    }

    if args.output:
        args.output.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf8")
    else:
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
