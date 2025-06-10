# RiskWise Analytics - Backend

This is the backend service for the RiskWise Analytics platform, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **Market Data API**: Endpoints for accessing market data, indices, and valuations
- **Authentication**: JWT-based authentication system
- **Database**: Async PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database migrations
- **Validation**: Pydantic models for request/response validation
- **Documentation**: Auto-generated API documentation with Swagger UI and ReDoc

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Redis (for caching, optional)
- pip (Python package manager)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/riskwise-analytics.git
   cd riskwise-analytics/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Copy the example environment file and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your database credentials and other settings.

5. **Initialize the database**
   ```bash
   # Create the database in PostgreSQL first
   createdb riskwise
   
   # Run migrations
   alembic upgrade head
   
   # Initialize with sample data
   python -m scripts.init_db
   ```

## Running the Application

### Development

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production

For production, use a production-ready ASGI server like Uvicorn with Gunicorn:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── alembic.ini           # Alembic configuration
├── requirements.txt       # Project dependencies
├── .env.example          # Example environment variables
├── scripts/              # Utility scripts
│   ├── init_db.py        # Initialize database with sample data
│   └── run.py            # Script to run the application
└── app/                  # Application package
    ├── __init__.py
    ├── main.py           # FastAPI application
    ├── core/             # Core functionality
    │   ├── __init__.py
    │   └── config.py     # Application configuration
    ├── db/               # Database configuration
    │   ├── __init__.py
    │   └── base.py       # Database connection and session
    ├── models/           # SQLAlchemy models
    │   ├── __init__.py
    │   └── market.py     # Market data models
    ├── schemas/          # Pydantic models
    │   ├── __init__.py
    │   └── market.py     # Market data schemas
    ├── services/         # Business logic
    │   ├── __init__.py
    │   ├── base.py       # Base service class
    │   └── market.py     # Market data services
    └── api/              # API routes
        ├── __init__.py
        ├── deps.py       # Dependencies
        └── api_v1/       # API v1
            ├── __init__.py
            ├── api.py    # API router
            └── endpoints/
                ├── __init__.py
                └── market.py  # Market data endpoints
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Linting

```bash
flake8
mypy .
```

## Deployment

### Docker

1. Build the Docker image:
   ```bash
   docker build -t riskwise-backend .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env riskwise-backend
   ```

### Kubernetes

Example Kubernetes deployment files are provided in the `k8s/` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
