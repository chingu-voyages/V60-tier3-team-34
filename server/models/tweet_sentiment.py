import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from models.base import Base


class SentimentType(str, enum.Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class TweetSentiment(Base):
    __tablename__ = "tweet_sentiments"

    id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    tweet_timestamp: Mapped[str] = mapped_column(
        String,
        ForeignKey("tweets.tweet_timestamp", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    sentiment: Mapped[SentimentType] = mapped_column(
        SQLEnum(SentimentType),
        nullable=False
    )
    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    stock_tickers: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list
    )
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
