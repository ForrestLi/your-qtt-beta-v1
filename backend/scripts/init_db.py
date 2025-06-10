import asyncio
import logging
from pathlib import Path
import sys

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.db.base import Base, async_engine, sync_engine, sync_session_factory
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_models():
    """Initialize database models (create tables)."""
    logger.info("Creating database tables...")
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import market
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully.")

def init_data():
    """Initialize initial data in the database."""
    from sqlalchemy.orm import Session
    from app.models.market import MarketIndex
    
    logger.info("Initializing initial data...")
    
    # Initialize common market indices
    indices = [
        {
            "symbol": "^GSPC",
            "name": "S&P 500",
            "description": "S&P 500 Index - US Large Cap Stocks",
            "region": "US",
            "currency": "USD",
            "is_active": True,
        },
        {
            "symbol": "^DJI",
            "name": "Dow Jones Industrial Average",
            "description": "Price-weighted average of 30 significant stocks traded on the NYSE and NASDAQ",
            "region": "US",
            "currency": "USD",
            "is_active": True,
        },
        {
            "symbol": "^IXIC",
            "name": "NASDAQ Composite",
            "description": "Market-capitalization weighted index of more than 3,000 stocks listed on the NASDAQ",
            "region": "US",
            "currency": "USD",
            "is_active": True,
        },
        {
            "symbol": "^GDAXI",
            "name": "DAX Performance Index",
            "description": "Blue chip stock market index of 30 major German companies trading on the Frankfurt Stock Exchange",
            "region": "DE",
            "currency": "EUR",
            "is_active": True,
        },
        {
            "symbol": "^FTSE",
            "name": "FTSE 100 Index",
            "description": "Share index of the 100 companies listed on the London Stock Exchange with the highest market capitalization",
            "region": "UK",
            "currency": "GBP",
            "is_active": True,
        },
    ]
    
    with sync_session_factory() as db:
        # Add indices if they don't exist
        for index_data in indices:
            existing = db.query(MarketIndex).filter_by(symbol=index_data["symbol"]).first()
            if not existing:
                db_index = MarketIndex(**index_data)
                db.add(db_index)
                logger.info(f"Added index: {index_data['symbol']} - {index_data['name']}")
        
        db.commit()
    
    logger.info("Initial data initialization complete.")

if __name__ == "__main__":
    # Create database tables
    asyncio.run(init_models())
    
    # Initialize initial data
    init_data()
    
    logger.info("Database initialization complete.")
