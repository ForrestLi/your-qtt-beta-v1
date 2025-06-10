from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class MarketIndexBase(BaseModel):
    """Base schema for market indices"""
    symbol: str = Field(..., max_length=20, example="^GSPC")
    name: str = Field(..., max_length=100, example="S&P 500")
    description: Optional[str] = Field(None, max_length=500)
    region: Optional[str] = Field(None, max_length=50, example="US")
    currency: str = Field("USD", max_length=10)
    is_active: bool = Field(True, description="Whether the index is actively tracked")


class MarketIndexCreate(MarketIndexBase):
    """Schema for creating a new market index"""
    pass


class MarketIndexUpdate(MarketIndexBase):
    """Schema for updating an existing market index"""
    symbol: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=100)
    currency: Optional[str] = Field(None, max_length=10)


class MarketIndexInDBBase(MarketIndexBase):
    """Base schema for market index in database"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MarketIndex(MarketIndexInDBBase):
    """Schema for returning a market index"""
    pass


class MarketDataBase(BaseModel):
    """Base schema for market data points"""
    index_id: int
    date: datetime
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: float
    volume: Optional[float] = None
    adjusted_close: Optional[float] = None


class MarketDataCreate(MarketDataBase):
    """Schema for creating a new market data point"""
    pass


class MarketDataInDBBase(MarketDataBase):
    """Base schema for market data in database"""
    id: int

    class Config:
        from_attributes = True


class MarketData(MarketDataInDBBase):
    """Schema for returning market data"""
    pass


class MarketValuationBase(BaseModel):
    """Base schema for market valuation metrics"""
    index_id: int
    date: datetime
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_yield: Optional[float] = None
    cape_ratio: Optional[float] = None
    market_cap: Optional[float] = None
    avg_volume: Optional[float] = None
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MarketValuationCreate(MarketValuationBase):
    """Schema for creating new market valuation metrics"""
    pass


class MarketValuationInDBBase(MarketValuationBase):
    """Base schema for market valuation in database"""
    id: int

    class Config:
        from_attributes = True


class MarketValuation(MarketValuationInDBBase):
    """Schema for returning market valuation metrics"""
    pass


class MarketSentimentBase(BaseModel):
    """Base schema for market sentiment indicators"""
    index_id: int
    date: datetime
    fear_greed_index: Optional[float] = Field(None, ge=0, le=100)
    vix: Optional[float] = None
    put_call_ratio: Optional[float] = None
    source: Optional[str] = None


class MarketSentimentCreate(MarketSentimentBase):
    """Schema for creating new market sentiment data"""
    pass


class MarketSentimentInDBBase(MarketSentimentBase):
    """Base schema for market sentiment in database"""
    id: int

    class Config:
        from_attributes = True


class MarketSentiment(MarketSentimentInDBBase):
    """Schema for returning market sentiment data"""
    pass


class Timeframe(str, Enum):
    """Timeframe for market data analysis"""
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1m"
    THREE_MONTHS = "3m"
    SIX_MONTHS = "6m"
    ONE_YEAR = "1y"
    THREE_YEARS = "3y"
    FIVE_YEARS = "5y"
    TEN_YEARS = "10y"
    TWENTY_YEARS = "20y"
    ALL = "all"


class MarketAnalysisRequest(BaseModel):
    """Request schema for market analysis"""
    symbol: str = Field(..., description="Market index symbol")
    timeframe: Timeframe = Field(Timeframe.ONE_YEAR, description="Analysis timeframe")
    metrics: List[str] = Field(
        default_factory=lambda: ["pe_ratio", "pb_ratio", "dividend_yield"],
        description="List of metrics to include in the analysis"
    )


class MarketAnalysisResponse(BaseModel):
    """Response schema for market analysis"""
    symbol: str
    name: str
    timeframe: str
    current_price: float
    currency: str
    metrics: Dict[str, Any]
    percentiles: Dict[str, float]
    recommendation: str
    confidence: float
    last_updated: datetime
