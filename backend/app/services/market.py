from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select, and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market import MarketIndex, MarketData, MarketValuation, MarketSentiment
from app.schemas.market import (
    MarketIndexCreate, MarketIndexUpdate, MarketDataCreate, 
    MarketValuationCreate, MarketSentimentCreate, Timeframe, MarketAnalysisRequest, MarketAnalysisResponse
)
from app.core.config import settings
from app.services.base import BaseService

class MarketService(BaseService[MarketIndex, MarketIndexCreate, MarketIndexUpdate]):
    """Service for market index operations"""
    
    async def get_by_symbol(self, db: AsyncSession, *, symbol: str) -> Optional[MarketIndex]:
        """Get a market index by symbol"""
        result = await db.execute(
            select(self.model).where(self.model.symbol == symbol.upper())
        )
        return result.scalars().first()
    
    async def get_active_indices(self, db: AsyncSession) -> List[MarketIndex]:
        """Get all active market indices"""
        result = await db.execute(
            select(self.model)
            .where(self.model.is_active == True)  # noqa: E712
            .order_by(self.model.symbol)
        )
        return result.scalars().all()


class MarketDataService(BaseService[MarketData, MarketDataCreate, MarketDataCreate]):
    """Service for market data operations"""
    
    async def get_latest_data(
        self, 
        db: AsyncSession, 
        *, 
        index_id: int,
        limit: int = 1
    ) -> List[MarketData]:
        """Get the latest market data for an index"""
        result = await db.execute(
            select(self.model)
            .where(self.model.index_id == index_id)
            .order_by(self.model.date.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_historical_data(
        self,
        db: AsyncSession,
        *,
        index_id: int,
        start_date: datetime,
        end_date: Optional[datetime] = None,
    ) -> List[MarketData]:
        """Get historical market data for an index within a date range"""
        query = select(self.model).where(
            and_(
                self.model.index_id == index_id,
                self.model.date >= start_date,
                self.model.date <= (end_date or datetime.utcnow())
            )
        ).order_by(self.model.date.asc())
        
        result = await db.execute(query)
        return result.scalars().all()


class MarketValuationService(BaseService[MarketValuation, MarketValuationCreate, MarketValuationCreate]):
    """Service for market valuation operations"""
    
    async def get_latest_valuation(
        self, 
        db: AsyncSession, 
        *, 
        index_id: int,
        limit: int = 1
    ) -> List[MarketValuation]:
        """Get the latest valuation for an index"""
        result = await db.execute(
            select(self.model)
            .where(self.model.index_id == index_id)
            .order_by(self.model.date.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_historical_valuations(
        self,
        db: AsyncSession,
        *,
        index_id: int,
        start_date: datetime,
        end_date: Optional[datetime] = None,
    ) -> List[MarketValuation]:
        """Get historical valuations for an index within a date range"""
        query = select(self.model).where(
            and_(
                self.model.index_id == index_id,
                self.model.date >= start_date,
                self.model.date <= (end_date or datetime.utcnow())
            )
        ).order_by(self.model.date.asc())
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def calculate_pe_percentile(
        self,
        db: AsyncSession,
        *,
        index_id: int,
        current_pe: float,
        years: int = 10
    ) -> float:
        """Calculate the percentile of the current PE ratio compared to historical data"""
        # Calculate the date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=365 * years)
        
        # Get all PE ratios within the date range
        result = await db.execute(
            select(self.model.pe_ratio)
            .where(
                and_(
                    self.model.index_id == index_id,
                    self.model.date >= start_date,
                    self.model.date <= end_date,
                    self.model.pe_ratio.isnot(None)
                )
            )
        )
        
        pe_ratios = [row[0] for row in result.all()]
        
        if not pe_ratios:
            return 50.0  # Default to median if no historical data
        
        # Calculate percentile
        lower_count = sum(1 for pe in pe_ratios if pe <= current_pe)
        percentile = (lower_count / len(pe_ratios)) * 100
        
        return round(percentile, 2)


class MarketAnalysisService:
    """Service for market analysis operations"""
    
    def __init__(self):
        self.market_index_service = MarketService(MarketIndex)
        self.market_data_service = MarketDataService(MarketData)
        self.valuation_service = MarketValuationService(MarketValuation)
    
    async def analyze_market(
        self,
        db: AsyncSession,
        *,
        request: MarketAnalysisRequest
    ) -> MarketAnalysisResponse:
        """Perform market analysis for the given symbol and timeframe"""
        # Get the market index
        index = await self.market_index_service.get_by_symbol(db, symbol=request.symbol)
        if not index:
            raise ValueError(f"Market index with symbol {request.symbol} not found")
        
        # Get the latest market data
        latest_data = await self.market_data_service.get_latest_data(db, index_id=index.id)
        if not latest_data:
            raise ValueError(f"No market data available for {index.symbol}")
        
        latest_close = latest_data[0].close
        
        # Get the latest valuation
        latest_valuation = await self.valuation_service.get_latest_valuation(db, index_id=index.id)
        if not latest_valuation:
            raise ValueError(f"No valuation data available for {index.symbol}")
        
        latest_pe = latest_valuation[0].pe_ratio
        
        # Calculate PE percentile
        pe_percentile = await self.valuation_service.calculate_pe_percentile(
            db, 
            index_id=index.id,
            current_pe=latest_pe,
            years=10
        )
        
        # Generate analysis
        analysis = self._generate_analysis(
            pe_ratio=latest_pe,
            pe_percentile=pe_percentile,
            index_name=index.name
        )
        
        # Prepare response
        return MarketAnalysisResponse(
            symbol=index.symbol,
            name=index.name,
            timeframe=request.timeframe,
            current_price=latest_close,
            currency=index.currency,
            metrics={
                "pe_ratio": latest_pe,
                "pe_percentile": pe_percentile,
                "dividend_yield": latest_valuation[0].dividend_yield,
                "pb_ratio": latest_valuation[0].pb_ratio,
            },
            percentiles={
                "pe": pe_percentile,
            },
            recommendation=analysis["recommendation"],
            confidence=analysis["confidence"],
            last_updated=datetime.utcnow()
        )
    
    def _generate_analysis(
        self,
        pe_ratio: float,
        pe_percentile: float,
        index_name: str
    ) -> Dict[str, Union[str, float]]:
        """Generate analysis based on market metrics"""
        if pe_ratio is None:
            return {
                "recommendation": "Insufficient data for analysis",
                "confidence": 0.0
            }
        
        if pe_percentile > 80:
            return {
                "recommendation": f"{index_name} appears overvalued based on historical PE ratios",
                "confidence": min(0.9, 0.5 + (pe_percentile - 80) / 40)  # Scale confidence from 0.5 to 0.9
            }
        elif pe_percentile < 20:
            return {
                "recommendation": f"{index_name} appears undervalued based on historical PE ratios",
                "confidence": min(0.9, 0.5 + (20 - pe_percentile) / 40)  # Scale confidence from 0.5 to 0.9
            }
        else:
            return {
                "recommendation": f"{index_name} appears fairly valued based on historical PE ratios",
                "confidence": 0.7  # Moderate confidence for neutral position
            }


# Create service instances
market_index_service = MarketService(MarketIndex)
market_data_service = MarketDataService(MarketData)
market_valuation_service = MarketValuationService(MarketValuation)
market_analysis_service = MarketAnalysisService()
