# Coffee Fortune Server - Deployment Guide

## Configuration Summary

### API Configuration
- **Model**: `google/gemini-2.0-flash-exp:free`
- **API Provider**: OpenRouter.ai
- **API Key**: Configured in `.env` file
- **Supported Languages**: English (en), Persian/Farsi (fa)

## Prerequisites

1. **Docker Desktop** installed and running
2. **Git** (for version control)

## Deployment Steps

### 1. Run the Setup Script

For Windows:
```bash
setup.bat
```

This script will:
- Check if Docker is installed
- Create `.env` file from template (if not exists)
- Build Docker images
- Start all services (PostgreSQL, Redis, Web, Celery)
- Run database migrations

### 2. Verify Services

After setup completes, verify all services are running:
```bash
docker-compose ps
```

You should see:
- `db` (PostgreSQL) - healthy
- `redis` - healthy
- `web` (Django API) - running on port 8000
- `celery` (Background worker) - running
- `celery-beat` (Scheduler) - running

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/

### 4. Create Admin User

To create a superuser for the admin panel:
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Initialize Fortune Features

Run the management command to populate fortune-telling features:
```bash
docker-compose exec web python manage.py populate_features
```

This will create the following features:
- Coffee Fortune Reading
- Feng Shui Analysis
- Dream Interpretation
- Birthdate Horoscope
- Tarot Reading
- Numerology
- Palm Reading

## Language Support

### Using Persian (Farsi) Language

When creating a reading via API, include the `language` parameter:

**Example API Request**:
```json
{
  "feature_type": "coffee_fortune",
  "text_input": "Your input text here",
  "language": "fa"
}
```

**Supported Language Codes**:
- `en` - English (default)
- `fa` - Persian (Farsi)

When `language` is set to `"fa"`, the AI model will:
- Respond in Persian script
- Use culturally appropriate context for Iranian/Persian traditions
- Maintain proper Persian language formatting

## API Endpoints

### Authentication
- `POST /api/accounts/request-otp/` - Request OTP code
- `POST /api/accounts/verify-otp/` - Verify OTP and get JWT tokens
- `POST /api/accounts/refresh/` - Refresh access token

### Fortune Features
- `GET /api/fortune/features/` - List all available features
- `GET /api/fortune/features/{id}/` - Get feature details
- `GET /api/fortune/features/by_type/?type=coffee_fortune` - Get feature by type

### Readings
- `POST /api/fortune/readings/` - Create new reading
- `GET /api/fortune/readings/` - List user's readings
- `GET /api/fortune/readings/{id}/` - Get reading details
- `GET /api/fortune/readings/{id}/status_check/` - Check reading status
- `POST /api/fortune/readings/{id}/feedback/` - Submit feedback
- `GET /api/fortune/readings/recent/` - Get recent readings

### Reading History
- `GET /api/fortune/history/` - List reading history
- `GET /api/fortune/history/statistics/` - Get user statistics

## Example: Creating a Coffee Fortune Reading in Persian

### Request:
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "feature_type=coffee_fortune" \
  -F "language=fa" \
  -F "image=@/path/to/coffee-cup.jpg"
```

### Response:
```json
{
  "id": "uuid-here",
  "feature": {
    "id": "feature-uuid",
    "name": "Coffee Fortune Reading",
    "feature_type": "coffee_fortune",
    "input_type": "image"
  },
  "language": "fa",
  "status": "pending",
  "created_at": "2025-10-12T10:30:00Z"
}
```

The interpretation will be generated in Persian and can be retrieved by checking the reading status or fetching the reading again once status is "completed".

## Managing the Application

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Run Database Migrations
```bash
docker-compose exec web python manage.py migrate
```

## Configuration Files

### `.env` File
Contains environment variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `OPENROUTER_API_KEY` - Your OpenRouter.ai API key
- `OTP_EXPIRY_SECONDS` - OTP expiration time
- `SMS_API_KEY` - SMS provider API key (for OTP delivery)

### `docker-compose.yml`
Defines all services and their configuration.

## Troubleshooting

### Issue: Services won't start
**Solution**: Make sure Docker Desktop is running and check logs:
```bash
docker-compose logs
```

### Issue: Database connection errors
**Solution**: Wait for PostgreSQL to be fully initialized:
```bash
docker-compose logs db
```

### Issue: API key not working
**Solution**: Verify the API key is correctly set in `.env` file and restart services:
```bash
docker-compose restart
```

### Issue: Persian text not displaying correctly
**Solution**: Ensure your client application supports UTF-8 encoding and RTL (right-to-left) text rendering.

## Security Notes

1. **Change the SECRET_KEY** in production
2. **Set DEBUG=False** in production
3. **Configure CORS** properly for production (update `CORS_ALLOW_ALL_ORIGINS` in settings.py)
4. **Use HTTPS** in production
5. **Secure your API key** - never commit it to version control
6. **Set up proper firewall rules** for production servers

## Support & Documentation

- **OpenRouter.ai Documentation**: https://openrouter.ai/docs
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Celery Documentation**: https://docs.celeryq.dev/

## Updates & Maintenance

### Update Model Configuration
To change the AI model, update the `model_name` field for features in the admin panel or directly in the database.

### Add More Languages
1. Edit `fortune/models.py` - add language to `SUPPORTED_LANGUAGES`
2. Edit `fortune/tasks.py` - add language instruction to `language_instructions` dict
3. Run migrations
4. Update API documentation

## Production Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up SSL/HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up SMS provider for OTP
- [ ] Configure domain name
- [ ] Set up firewall rules
- [ ] Review security settings
