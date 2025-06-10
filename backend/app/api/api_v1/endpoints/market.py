from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps
from app.db.base import get_db
from app.services.market import (
    market_index_service,
    market_data_service,
    market_valuation_service,
    market_analysis_service
)

router = APIRouter()

# Market Indices
@router.get("/indices/", response_model=List[schemas.MarketIndex])
async def read_indices(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve market indices.
    """
    indices = await market_index_service.get_multi(db, skip=skip, limit=limit)
    return indices


@router.get("/indices/active/", response_model=List[schemas.MarketIndex])
async def read_active_indices(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve active market indices.
    """
    return await market_index_service.get_active_indices(db)


@router.get("/indices/{symbol}", response_model=schemas.MarketIndex)
async def read_index_by_symbol(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific market index by symbol.
    """
    index = await market_index_service.get_by_symbol(db, symbol=symbol.upper())
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market index with symbol {symbol} not found",
        )
    return index


# Market Data
@router.get("/market-data/{symbol}/latest/", response_model=List[schemas.MarketData])
async def read_latest_market_data(
    symbol: str,
    limit: int = Query(1, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the latest market data for a specific index.
    """
    index = await market_index_service.get_by_symbol(db, symbol=symbol.upper())
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market index with symbol {symbol} not found",
        )
    
    data = await market_data_service.get_latest_data(
        db, index_id=index.id, limit=limit
    )
    return data


@router.get("/market-data/{symbol}/historical/", response_model=List[schemas.MarketData])
async def read_historical_market_data(
    symbol: str,
    start_date: datetime,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get historical market data for a specific index within a date range.
    """
    index = await market_index_service.get_by_symbol(db, symbol=symbol.upper())
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market index with symbol {symbol} not found",
        )
    
    data = await market_data_service.get_historical_data(
        db, index_id=index.id, start_date=start_date, end_date=end_date
    )
    return data


# Market Valuations
@router.get("/valuations/{symbol}/latest/", response_model=List[schemas.MarketValuation])
async def read_latest_valuations(
    symbol: str,
    limit: int = Query(1, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the latest valuation metrics for a specific index.
    """
    index = await market_index_service.get_by_symbol(db, symbol=symbol.upper())
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market index with symbol {symbol} not found",
        )
    
    valuations = await market_valuation_service.get_latest_valuation(
        db, index_id=index.id, limit=limit
    )
    return valuations


@router.get("/valuations/{symbol}/pe-percentile/", response_model=Dict[str, float])
async def calculate_pe_percentile(
    symbol: str,
    years: int = Query(10, ge=1, le=50, description="Number of years of historical data to consider"),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Calculate the percentile of the current PE ratio compared to historical data.
    """
    index = await market_index_service.get_by_symbol(db, symbol=symbol.upper())
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market index with symbol {symbol} not found",
        )
    
    # Get latest PE ratio
    latest_valuation = await market_valuation_service.get_latest_valuation(
        db, index_id=index.id, limit=1
    )
    
    if not latest_valuation or latest_valuation[0].pe_ratio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No PE ratio data available for {symbol}",
        )
    
    current_pe = latest_valuation[0].pe_ratio
    
    # Calculate percentile
    percentile = await market_valuation_service.calculate_pe_percentile(
        db, 
        index_id=index.id,
        current_pe=current_pe,
        years=years
    )
    
    return {
        "symbol": symbol,
        "pe_ratio": current_pe,
        "percentile": percentile,
        "years_considered": years,
    }


# Market Analysis
@router.get("/analysis/{symbol}", response_model=schemas.MarketAnalysisResponse)
async def analyze_market(
    symbol: str,
    timeframe: schemas.Timeframe = Query(
        schemas.Timeframe.ONE_YEAR, 
        description="Timeframe for the analysis"
    ),
    metrics: List[str] = Query(
        default=["pe_ratio", "pb_ratio", "dividend_yield"],
        description="List of metrics to include in the analysis"
    ),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Perform a comprehensive market analysis for the given symbol.
    """
    analysis_request = schemas.MarketAnalysisRequest(
        symbol=symbol,
        timeframe=timeframe,
        metrics=metrics
    )
    
    try:
        analysis = await market_analysis_service.analyze_market(
            db, request=analysis_request
        )
        return analysis
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# Market Sentiment
@router.get("/sentiment/{symbol}/latest/", response_model=List[schemas.MarketSentiment])
async def read_latest_sentiment(
    symbol: str,
    limit: int = Query(1, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the latest sentiment indicators for a specific index.
    """
    index = await market_index_service.get_by_symbol(db, symbol=symbol.upper())
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market index with symbol {symbol} not found",
        )
    
    # This is a placeholder - implement actual sentiment data retrieval
    # based on your data model
    return []


# Helper endpoint to get available timeframes
@router.get("/timeframes/", response_model=Dict[str, str])
async def get_available_timeframes() -> Any:
    """
    Get available timeframes for market analysis.
    """
    return {
        tf.value: tf.name.replace("_", " ").title() 
        for tf in schemas.Timeframe
    }
