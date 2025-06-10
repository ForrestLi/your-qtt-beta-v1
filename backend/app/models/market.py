from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

class MarketIndex(Base):
    """Market index model (e.g., S&P 500, NASDAQ, etc.)"""
    __tablename__ = "market_indices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    region = Column(String(50), nullable=True)
    currency = Column(String(10), nullable=False, default="USD")
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    data_points = relationship("MarketData", back_populates="index", cascade="all, delete-orphan")
    valuations = relationship("MarketValuation", back_populates="index", cascade="all, delete-orphan")


class MarketData(Base):
    """Historical market data points"""
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    index_id = Column(Integer, ForeignKey("market_indices.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)
    adjusted_close = Column(Float, nullable=True)
    
    # Relationships
    index = relationship("MarketIndex", back_populates="data_points")
    
    # Indexes
    __table_args__ = (
        Index('ix_market_data_index_date', 'index_id', 'date', unique=True),
    )


class MarketValuation(Base):
    """Market valuation metrics (PE, PB, etc.)"""
    __tablename__ = "market_valuations"
    
    id = Column(Integer, primary_key=True, index=True)
    index_id = Column(Integer, ForeignKey("market_indices.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Valuation metrics
    pe_ratio = Column(Float, nullable=True)
    pb_ratio = Column(Float, nullable=True)
    dividend_yield = Column(Float, nullable=True)
    earnings_yield = Column(Float, nullable=True)
    cape_ratio = Column(Float, nullable=True)  # Shiller PE
    
    # Additional metrics
    market_cap = Column(Float, nullable=True)
    avg_volume = Column(Float, nullable=True)
    
    # Metadata
    source = Column(String(50), nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True)
    
    # Relationships
    index = relationship("MarketIndex", back_populates="valuations")
    
    # Indexes
    __table_args__ = (
        Index('ix_market_valuations_index_date', 'index_id', 'date', unique=True),
    )


class MarketSentiment(Base):
    """Market sentiment indicators"""
    __tablename__ = "market_sentiments"
    
    id = Column(Integer, primary_key=True, index=True)
    index_id = Column(Integer, ForeignKey("market_indices.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Sentiment indicators
    fear_greed_index = Column(Float, nullable=True)  # 0-100
    vix = Column(Float, nullable=True)  # Volatility Index
    put_call_ratio = Column(Float, nullable=True)
    
    # Metadata
    source = Column(String(50), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('ix_market_sentiment_index_date', 'index_id', 'date', unique=True),
    )
