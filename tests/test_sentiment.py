from datetime import UTC, datetime

from social_listening.analysis.sentiment import analyze_post
from social_listening.models import Post


def make_post(text: str) -> Post:
    return Post(
        post_id="1",
        source="test",
        author_id="a",
        author="A",
        text=text,
        timestamp=datetime.now(UTC),
    )


def test_positive_sentiment():
    post = make_post("Servicio excelente y genial")
    analyzed = analyze_post(post)
    assert analyzed.sentiment_label == "positive"


def test_negative_sentiment():
    post = make_post("Demora horrible y pésimo servicio")
    analyzed = analyze_post(post)
    assert analyzed.sentiment_label == "negative"


def test_neutral_sentiment():
    post = make_post("El paquete llegó")
    analyzed = analyze_post(post)
    assert analyzed.sentiment_label == "neutral"
