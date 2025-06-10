# RiskWise Analytics: Smart Risk Hedging Platform

![RiskWise Analytics Dashboard](./screenshot.png)

RiskWise Analytics is a next-generation investment platform specializing in intelligent risk hedging across three dimensions: Market Beta, Stock Alpha, and Strategy Fitness.

## Features

### Phase 1: Market Beta Engine (Current Focus)
- Real-time market data visualization
- Historical PE ratio analysis
- Market valuation percentiles
- Regression-based return forecasting

## Getting Started

### Prerequisites

- Node.js 18+
- npm 9+ or yarn 1.22+
- Python 3.10+ (for backend)
- MySQL 8.0+ (for database)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/riskwise-analytics.git
   cd riskwise-analytics
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open in browser**
   The application will be available at [http://localhost:5173](http://localhost:5173)

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── assets/          # Images, fonts, etc.
│   ├── components/       # Reusable Vue components
│   ├── composables/      # Vue 3 composables
│   ├── router/           # Vue Router configuration
│   ├── store/            # Pinia stores
│   ├── types/            # TypeScript type definitions
│   ├── views/            # Page components
│   ├── App.vue           # Root component
│   └── main.ts           # Application entry point
├── .env                  # Environment variables
├── index.html            # Main HTML file
```

## Development

### Backend Development

- Run tests:
  ```bash
  cd backend
  pytest
  ```

- Generate migrations:
  ```bash
  alembic revision --autogenerate -m "Your migration message"
  ```

- Apply migrations:
  ```bash
  alembic upgrade head
  ```

### Frontend Development

- Run linter:
  ```bash
  cd frontend
  npm run lint
  ```

- Format code:
  ```bash
  npm run format
  ```

## Deployment

### Production Build

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. The production-ready files will be in the `frontend/dist` directory.

### Docker Production

Build and run the production containers:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Application environment | `development` |
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Secret key for JWT | - |
| `DATABASE_URL` | Database connection URL | - |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Base URL for API requests | `http://localhost:8000/api/v1` |
| `VITE_APP_TITLE` | Application title | `RiskWise Analytics` |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Vue.js](https://vuejs.org/)
- [Vite](https://vitejs.dev/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)
