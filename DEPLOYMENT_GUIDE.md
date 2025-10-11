# Coffee Fortune Server - Deployment Guide

Complete guide for setting up and deploying the Coffee Fortune Server backend.

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Initial Setup](#initial-setup)
4. [Database Setup](#database-setup)
5. [Populating Features](#populating-features)
6. [Running the Server](#running-the-server)
7. [Testing the API](#testing-the-api)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

Get the server running in under 5 minutes with Docker:

```bash
# 1. Start all services
docker-compose up -d --build

# 2. Run migrations
docker-compose exec web python manage.py migrate

# 3. Populate fortune features
docker-compose exec web python manage.py populate_features

# 4. Check API status
docker-compose exec web python manage.py check_api_status

# 5. Create superuser (optional)
docker-compose exec web python manage.py createsuperuser

# Done! API is running at http://localhost:8000
```

---

## System Requirements

### With Docker (Recommended)
- Docker Desktop or Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB free disk space

### Without Docker
- Python 3.10 or higher
- PostgreSQL 13+ (or SQLite for development)
- Redis 6.0+
- 2GB RAM minimum

---

## Initial Setup

### 1. Clone or Download the Project

```bash
cd coffee-fortune-server
```

### 2. Environment Configuration

The `.env` file is already configured for development. Key settings:

```env
# Basic Settings
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# Database (Docker)
DATABASE_URL=postgresql://postgres:postgres@db:5432/coffee_fortune_db

# Redis & Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

# OpenRouter.ai (Optional for testing)
OPENROUTER_API_KEY=
```

**For Production:** Update these values in `.env`:
- Set `DEBUG=False`
- Change `SECRET_KEY` to a strong random value
- Configure proper `DATABASE_URL` with secure credentials
- Set `OPENROUTER_API_KEY` for real AI-powered readings

### 3. Get OpenRouter.ai API Key (Optional)

The system works in MOCK MODE without an API key, perfect for:
- Frontend development
- Testing the API structure
- Demo purposes

To enable real AI-powered fortune readings:

1. Visit [OpenRouter.ai](https://openrouter.ai/keys)
2. Create an account
3. Generate an API key
4. Add to `.env`: `OPENROUTER_API_KEY=your-key-here`
5. Restart the application

---

## Database Setup

### With Docker (Automatic)

Docker Compose automatically sets up PostgreSQL:

```bash
docker-compose up -d db
```

### Without Docker (Manual)

#### PostgreSQL Setup

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE coffee_fortune_db;
CREATE USER coffee_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE coffee_fortune_db TO coffee_user;
\q

# Update .env
DATABASE_URL=postgresql://coffee_user:your_password@localhost:5432/coffee_fortune_db
```

#### SQLite Setup (Development Only)

```bash
# Update .env
DATABASE_URL=sqlite:///db.sqlite3
```

### Run Migrations

```bash
# With Docker
docker-compose exec web python manage.py migrate

# Without Docker
python manage.py migrate
```

---

## Populating Features

Load the pre-configured fortune-telling features into the database:

```bash
# With Docker
docker-compose exec web python manage.py populate_features

# Without Docker
python manage.py populate_features
```

This creates 7 fortune features:
1. ☕ Coffee Fortune Reading (image)
2. 🏠 Feng Shui Room Analysis (image)
3. 💭 Dream Interpretation (text)
4. 🎂 Birthdate Horoscope (text)
5. 🔮 Tarot Reading (text)
6. 🔢 Numerology Analysis (text)
7. ✋ Palm Reading (image)

**Output:**
```
✓ Created: Coffee Fortune Reading
✓ Created: Feng Shui Room Analysis
✓ Created: Dream Interpretation
...
Completed! Created: 7, Updated: 0
```

---

## Running the Server

### With Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services included:
- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)
- **celery**: Celery worker for async tasks

### Without Docker

#### Terminal 1 - Redis
```bash
redis-server
```

#### Terminal 2 - Celery Worker
```bash
celery -A config worker -l info
```

#### Terminal 3 - Django Server
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Testing the API

### 1. Check System Status

```bash
# With Docker
docker-compose exec web python manage.py check_api_status

# Without Docker
python manage.py check_api_status
```

This shows:
- API key configuration status
- Number of features loaded
- API connection status (if key configured)

### 2. Access Admin Panel

Create a superuser first:

```bash
# With Docker
docker-compose exec web python manage.py createsuperuser

# Without Docker
python manage.py createsuperuser
```

Then visit: http://localhost:8000/admin

### 3. Test Authentication API

#### Send OTP
```bash
curl -X POST http://localhost:8000/api/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

#### Check Celery logs for OTP (development mode)
```bash
docker-compose logs -f celery
# Look for: [DEBUG MODE] OTP for +1234567890: 123456
```

#### Verify OTP
```bash
curl -X POST http://localhost:8000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "otp_code": "123456"
  }'
```

Save the `access` token from the response.

### 4. Test Fortune Features

#### List Features
```bash
curl -X GET http://localhost:8000/api/fortune/features/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Create Dream Interpretation
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "text_input": "I dreamed I was flying over the ocean and saw a beautiful lighthouse."
  }'
```

#### Check Reading Status
```bash
# Wait a few seconds, then:
curl -X GET http://localhost:8000/api/fortune/readings/READING_ID/status_check/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Test Image Upload (Coffee Fortune)

```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "feature_type=coffee_fortune" \
  -F "image=@/path/to/your/coffee_cup.jpg"
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Update `.env` with production values:
  - [ ] `DEBUG=False`
  - [ ] Strong `SECRET_KEY`
  - [ ] Secure database credentials
  - [ ] Configure `ALLOWED_HOSTS`
  - [ ] Set `OPENROUTER_API_KEY`
- [ ] Update CORS settings in `config/settings.py`
- [ ] Set up proper firewall rules
- [ ] Configure SSL/HTTPS
- [ ] Set up database backups
- [ ] Configure Redis persistence
- [ ] Set up monitoring and logging

### Deployment Options

#### Option 1: Docker Compose (VPS/Cloud)

```bash
# On your server
git clone your-repo
cd coffee-fortune-server

# Update .env for production
nano .env

# Deploy
docker-compose -f docker-compose.yml up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Populate features
docker-compose exec web python manage.py populate_features

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

#### Option 2: Platform as a Service

Suitable for: Heroku, Railway, Render, DigitalOcean App Platform

1. Add `Procfile`:
```
web: gunicorn config.wsgi:application
worker: celery -A config worker -l info
```

2. Configure environment variables in platform dashboard

3. Add Redis and PostgreSQL add-ons

4. Deploy via Git push or GitHub integration

#### Option 3: Kubernetes

A sample Kubernetes configuration would include:
- Deployment for Django application
- StatefulSet for PostgreSQL
- Deployment for Redis
- Deployment for Celery workers
- Services and Ingress configuration

(Contact for detailed k8s manifests if needed)

### Post-Deployment

```bash
# Verify deployment
curl https://your-domain.com/api/fortune/features/

# Monitor logs
docker-compose logs -f web
docker-compose logs -f celery

# Check system status
docker-compose exec web python manage.py check_api_status
```

---

## Troubleshooting

### Issue: Database connection errors

```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Issue: Celery not processing tasks

```bash
# Check Celery worker
docker-compose logs celery

# Restart Celery
docker-compose restart celery

# Test Redis connection
docker-compose exec redis redis-cli ping
# Should return: PONG
```

### Issue: OTP not received

**In Development:**
- OTPs are logged to console (not sent via SMS)
- Check: `docker-compose logs -f celery`
- Look for: `[DEBUG MODE] OTP for +xxx: 123456`

**In Production:**
- Configure SMS provider settings in `.env`
- Update `accounts/tasks.py` with SMS integration

### Issue: Images not uploading

```bash
# Check media directory permissions
ls -la media/

# Ensure MEDIA_ROOT is writable
chmod -R 755 media/

# Check Docker volume
docker-compose exec web ls -la /app/media
```

### Issue: API returns 401 Unauthorized

- Check if token is included in Authorization header
- Verify token hasn't expired (24 hours for access tokens)
- Use refresh token endpoint to get new access token

### Issue: Readings stuck in "processing" status

```bash
# Check Celery worker logs
docker-compose logs celery

# Check if OpenRouter API is working
docker-compose exec web python manage.py check_api_status

# Restart Celery worker
docker-compose restart celery
```

### Issue: Features not appearing

```bash
# Run populate command again
docker-compose exec web python manage.py populate_features

# Check in Django admin
# Visit: http://localhost:8000/admin/fortune/fortunefeature/
```

---

## Monitoring and Maintenance

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f db
```

### Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U postgres coffee_fortune_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres coffee_fortune_db < backup.sql
```

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate
```

### Clean Up Old Data

```bash
# Manual cleanup of old failed readings
docker-compose exec web python manage.py shell

>>> from fortune.models import Reading
>>> from django.utils import timezone
>>> from datetime import timedelta
>>> cutoff = timezone.now() - timedelta(days=30)
>>> Reading.objects.filter(status='failed', created_at__lt=cutoff).delete()
```

Or use the built-in Celery task (configure with Celery Beat).

---

## Performance Optimization

### Production Settings

1. **Enable connection pooling** (already configured)
2. **Use Gunicorn with multiple workers**
   ```bash
   gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
   ```
3. **Configure Redis persistence**
4. **Set up CDN for static/media files**
5. **Enable database query optimization**
6. **Configure Celery with appropriate concurrency**

### Scaling

- **Horizontal scaling**: Run multiple Django containers behind a load balancer
- **Celery workers**: Scale workers based on queue length
- **Database**: Consider PostgreSQL read replicas for high traffic
- **Redis**: Use Redis Cluster for high availability

---

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to version control
2. **HTTPS**: Always use SSL/TLS in production
3. **CORS**: Restrict `CORS_ALLOW_ALL_ORIGINS` to specific domains
4. **Rate Limiting**: Implement per-user rate limits
5. **Authentication**: JWT tokens are secure, but consider refresh token rotation
6. **Input Validation**: Already implemented in serializers
7. **File Uploads**: Scan uploaded images for malware in production
8. **Database**: Use strong passwords and restrict network access
9. **Secrets Management**: Use vault services for sensitive data
10. **Logging**: Enable security event logging

---

## Support and Documentation

- **API Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for auth endpoints
- **Fortune API**: See [FORTUNE_API_DOCUMENTATION.md](FORTUNE_API_DOCUMENTATION.md)
- **Django Admin**: Access at `/admin/` for database management
- **Architecture**: Django + DRF + Celery + Redis + PostgreSQL

---

## Next Steps

1. ✅ Set up the development environment
2. ✅ Test all API endpoints
3. ✅ Configure OpenRouter.ai API key
4. 🔄 Integrate with frontend application
5. 🔄 Configure SMS provider for production
6. 🔄 Set up monitoring and alerts
7. 🔄 Plan production deployment
8. 🔄 Implement additional features

---

**Version:** 1.0.0
**Last Updated:** January 2025
