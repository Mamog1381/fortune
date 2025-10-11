#!/bin/bash

# Coffee Fortune Server - Docker Setup Script

echo "========================================"
echo "Coffee Fortune Server - Docker Setup"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "IMPORTANT: Please edit .env file and update the SECRET_KEY and other settings!"
    echo ""
else
    echo "✓ .env file already exists"
fi

echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "Running database migrations..."
docker-compose exec -T web python manage.py migrate

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Services are running:"
echo "  - Web API: http://localhost:8000"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo ""
echo "Check Celery logs for OTP codes (in DEBUG mode):"
echo "  docker-compose logs -f celery"
echo ""
