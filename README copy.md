# RiskWise Analytics: Smart Risk Hedging Platform

![RiskWise Logo](https://via.placeholder.com/150) *"See the risks before they see you"*

RiskWise Analytics is a next-generation investment platform specializing in intelligent risk hedging across three dimensions: Market Beta, Stock Alpha, and Strategy Fitness.

## Core Features

### 1. Market Beta Dashboard (Left Panel)
- Real-time valuation metrics for global markets:
  - US (S&P 500, NASDAQ)
  - HK (Hang Seng Index)
  - China A-shares (CSI 300)
  - Europe (Euro Stoxx 50)
  - Japan (Nikkei 225)
  - PE ratios with historical context
  - PB ratios and dividend yields
- Valuation percentiles across time horizons:
  - 3yr, 5yr, 10yr, 20yr, all-time
- Forward-looking return projections:
  - Statistical forecasts based on current valuation regimes
  - PE mean reversion analysis
  - Historical percentile analysis

### 2. Stock Alpha Analyzer (Center Panel)
- Buffett-inspired fundamental analysis:
  - ROE analysis
  - Debt-to-equity ratio
  - Free cash flow yield
  - PE ratio percentile
  - Revenue growth
  - Profit margin
- AI-Powered Risk Profiler:
  - Interactive questionnaires
  - Competitor benchmarking
  - Management quality assessment

### 3. Strategy Fitness Lab (Right Panel)
- Backtesting environment for:
  - Market-making strategies
  - Statistical arbitrage
  - Liquidity provision
- Latency Competitiveness Audit:
  - Microsecond-level performance analysis
  - Infrastructure requirements
  - Family office readiness assessment

## Technology Stack
- Frontend: React/TypeScript with D3.js
- Backend: Python FastAPI + MySQL for latency-sensitive modules
- Data: Snowflake + Redis for real-time analytics
- AI: Fine-tuned LLMs for risk assessment

## Getting Started

### Prerequisites

- **Node.js 18+** (for frontend development)
- **Python 3.10+** (for backend development)
- **MySQL 8.0+** (or compatible database)
- **Redis** (for caching and real-time features)
- **Git** (for version control)

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-qtt.git
cd your-qtt
```

#### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```
   
   **Note:** If you encounter issues with numpy installation, try:
   ```bash
   pip install numpy==1.24.3 --no-cache-dir
   pip install -r requirements.txt --no-cache-dir
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

#### 3. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update API endpoints if needed
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

### Running with Docker (Alternative)

If you prefer using Docker:

1. Ensure Docker and Docker Compose are installed
2. From the project root, run:
   ```bash
   docker compose up --build
   ```
3. Access the application at `http://localhost:3000`

### Troubleshooting

#### Python Package Installation Issues
- If you encounter `pkgutil` errors, try:
  ```bash
  python -m pip install --upgrade pip setuptools wheel
  ```

#### Database Connection Issues
- Verify MySQL is running and the credentials in `.env` are correct
- Ensure the database exists and the user has proper permissions

#### Frontend Build Issues
- Clear npm cache:
  ```bash
  npm cache clean --force
  rm -rf node_modules
  npm install
  ```

### Development Workflow

1. Make your changes in the appropriate directory
2. For backend changes, the server will auto-reload
3. For frontend changes, the development server will hot-reload
4. Run tests before committing:
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

## Deployment

For production deployment, consider using:
- **Backend**: Gunicorn with Uvicorn workers
- **Frontend**: Build and serve static files using Nginx
- **Database**: Managed database service (e.g., AWS RDS, Google Cloud SQL)
- **Caching**: Redis for session management and caching

## API Documentation

### Market Beta Analysis
```http
GET /api/v1/market-beta
```
Parameters:
- `market` (string): Market identifier (e.g., 'US', 'HK', 'CN')
- `timeframe` (string): Analysis timeframe ('3y', '5y', '10y', '20y', 'all')

### Alpha Analysis
```http
GET /api/v1/alpha-analysis
```
Parameters:
- `ticker` (string): Stock ticker
- `analysis_type` (string): Type of analysis ('owner_earnings', 'moat', 'safety')

### Strategy Fitness
```http
POST /api/v1/strategy-test
```
Request Body:
```json
{
  "strategy_type": "market_making",
  "parameters": {
    "spread": 0.01,
    "position_limit": 1000
  },
  "test_period": {
    "start": "2023-01-01",
    "end": "2023-12-31"
  }
}
```

## Development Roadmap

See [TASK.md](TASK.md) for detailed development phases and progress tracking.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with modern quantitative techniques and AI/ML
- Inspired by professional trading desks and family offices
- Powered by industry-leading data providers 