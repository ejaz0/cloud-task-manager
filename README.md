# CloudTask API

A production-ready FastAPI backend for task management.

## Features
- FastAPI with modular structure
- PostgreSQL + SQLAlchemy ORM
- Alembic migrations
- JWT Authentication & RBAC
- Redis caching
- Celery background tasks
- Prometheus metrics
- Structured logging
- Dockerized setup with Nginx proxy

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+

### Setup
1. Clone the repository
2. Run `sh scripts/init_env.sh` to setup your environment variables.
3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

### Development setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install .[dev]`

## API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
