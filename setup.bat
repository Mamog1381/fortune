@echo off
REM Coffee Fortune Server - Docker Setup Script for Windows

echo ========================================
echo Coffee Fortune Server - Docker Setup
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker Compose is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo [OK] .env file created
    echo.
    echo IMPORTANT: Please edit .env file and update the SECRET_KEY and other settings!
    echo.
) else (
    echo [OK] .env file already exists
)

echo Building Docker images...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo Running database migrations...
docker-compose exec -T web python manage.py migrate

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Services are running:
echo   - Web API: http://localhost:8000
echo   - PostgreSQL: localhost:5432
echo   - Redis: localhost:6379
echo.
echo Useful commands:
echo   - View logs: docker-compose logs -f
echo   - Create superuser: docker-compose exec web python manage.py createsuperuser
echo   - Stop services: docker-compose down
echo   - Restart services: docker-compose restart
echo.
echo Check Celery logs for OTP codes (in DEBUG mode):
echo   docker-compose logs -f celery
echo.
pause
