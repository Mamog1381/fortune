# Coffee Fortune Server

Django REST Framework backend server for Coffee Fortune mobile application - A mystical entertainment app featuring coffee fortune reading, dream interpretation, feng shui analysis, and more.

## Features

### Authentication & Security
- **OTP Authentication**: Phone number-based authentication with SMS OTP
- **JWT Tokens**: Secure authentication using Simple JWT
- **Brute-Force Protection**: Rate limiting and automatic blocking
- **Redis Caching**: OTP storage and session management

### Fortune-Telling Features
- ☕ **Coffee Fortune Reading**: AI-powered interpretation of coffee cup patterns (image)
- 🏠 **Feng Shui Analysis**: Room energy assessment and recommendations (image)
- 💭 **Dream Interpretation**: Detailed dream analysis and symbolism (text)
- 🎂 **Birthdate Horoscope**: Personalized astrology readings (text)
- 🔮 **Tarot Reading**: Three-card spread with guidance (text)
- 🔢 **Numerology**: Complete numerology profile (text)
- ✋ **Palm Reading**: Palmistry analysis from hand photos (image)

### Technical Features
- **Async Processing**: Celery workers for background task processing
- **AI Integration**: OpenRouter.ai for text and vision models
- **Image Upload**: Support for JPG, PNG, WEBP formats
- **Mock Mode**: Works without API key for development
- **Docker Support**: Complete containerized setup
- **Admin Panel**: Django admin for feature management

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework 3.14
- **Authentication**: Simple JWT 5.3
- **Task Queue**: Celery 5.3
- **Cache/Broker**: Redis 5.0
- **Database**: PostgreSQL 15
- **AI Service**: OpenRouter.ai API
- **Deployment**: Docker & Docker Compose
- **Image Processing**: Pillow 10.2

## Project Structure

```
coffee-fortune-server/
├── config/                     # Django project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL routing
│   ├── celery.py              # Celery configuration
│   ├── wsgi.py & asgi.py
├── accounts/                   # Authentication app
│   ├── models.py              # Custom User model
│   ├── views.py               # OTP auth views
│   ├── serializers.py         # Auth serializers
│   ├── tasks.py               # SMS sending tasks
│   ├── redis_protection.py    # Rate limiting
│   └── urls.py
├── fortune/                    # Fortune features app
│   ├── models.py              # FortuneFeature, Reading, History
│   ├── views.py               # Feature & reading views
│   ├── serializers.py         # Fortune serializers
│   ├── tasks.py               # Reading processing
│   ├── admin.py               # Admin configuration
│   ├── urls.py
│   ├── services/
│   │   ├── openrouter_service.py   # AI API integration
│   │   └── image_analyzer.py       # Image handling
│   └── management/commands/
│       ├── populate_features.py    # Load features
│       └── check_api_status.py     # Status checker
├── docker-compose.yml         # Container orchestration
├── Dockerfile
├── requirements.txt
├── .env                       # Environment config
├── README.md
├── QUICK_START.md            # 5-minute setup
├── DEPLOYMENT_GUIDE.md       # Full deployment docs
├── API_DOCUMENTATION.md      # Auth API docs
└── FORTUNE_API_DOCUMENTATION.md  # Fortune API docs
```

## Quick Start

See [QUICK_START.md](QUICK_START.md) for the fastest way to get started!

```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate_features
docker-compose exec web python manage.py check_api_status
```

Server runs at: **http://localhost:8000**

## Documentation

- 📚 **[Quick Start Guide](QUICK_START.md)** - Get running in 5 minutes
- 🚀 **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Complete setup and production deployment
- 🔐 **[Auth API Documentation](API_DOCUMENTATION.md)** - OTP authentication endpoints
- 🔮 **[Fortune API Documentation](FORTUNE_API_DOCUMENTATION.md)** - Fortune reading endpoints

## API Endpoints

### Authentication (OTP-based)

#### Send OTP
```http
POST /api/auth/send-otp/
Content-Type: application/json

{
    "phone_number": "+1234567890"
}
```

**Response:**
```json
{
    "message": "OTP sent successfully",
    "phone_number": "+1234567890",
    "expires_in": 300
}
```

#### Verify OTP
```http
POST /api/auth/verify/
Content-Type: application/json

{
    "phone_number": "+1234567890",
    "otp_code": "123456"
}
```

**Response:**
```json
{
    "message": "Authentication successful",
    "user": {
        "id": 1,
        "phone_number": "+1234567890",
        "first_name": "",
        "last_name": "",
        "date_joined": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Fortune Features

#### List Features
```http
GET /api/fortune/features/
Authorization: Bearer <token>
```

#### Create Reading (Text-based)
```http
POST /api/fortune/readings/
Authorization: Bearer <token>
Content-Type: application/json

{
  "feature_type": "dream_interpretation",
  "text_input": "Your dream or input here..."
}
```

#### Create Reading (Image-based)
```http
POST /api/fortune/readings/
Authorization: Bearer <token>
Content-Type: multipart/form-data

feature_type=coffee_fortune
image=<file>
```

#### Check Reading Status
```http
GET /api/fortune/readings/{id}/status_check/
Authorization: Bearer <token>
```

See [Fortune API Documentation](FORTUNE_API_DOCUMENTATION.md) for complete endpoint details.

## Setup Instructions

### Prerequisites

- **Docker Desktop** (Recommended) or Docker Engine + Docker Compose
- **4GB RAM** minimum
- **10GB disk space**

### Quick Setup (5 minutes)

```bash
# 1. Start services
docker-compose up -d --build

# 2. Initialize database
docker-compose exec web python manage.py migrate

# 3. Load fortune features (7 default features)
docker-compose exec web python manage.py populate_features

# 4. Check system status
docker-compose exec web python manage.py check_api_status

# 5. (Optional) Create admin user
docker-compose exec web python manage.py createsuperuser
```

**Done!** Your server is running at:
- 🌐 **API**: http://localhost:8000
- 🔐 **Admin Panel**: http://localhost:8000/admin

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f redis
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

## OpenRouter.ai API Key Configuration

The system works in **MOCK MODE** without an API key (perfect for testing!).

To enable real AI-powered fortune readings:

```bash
# 1. Get API key from https://openrouter.ai/keys
# 2. Add to .env file
OPENROUTER_API_KEY=your-key-here

# 3. Restart services
docker-compose restart web celery

# 4. Verify
docker-compose exec web python manage.py check_api_status
```

**Mock Mode Features:**
- ✅ All endpoints work normally
- ✅ Returns demonstration fortune readings
- ✅ Perfect for frontend development
- ✅ No costs or API limits

## Development Setup (Without Docker)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file
   ```

4. **Install and run Redis**
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install redis-server
   redis-server

   # On macOS
   brew install redis
   redis-server
   ```

5. **Install and run PostgreSQL**
   ```bash
   # Create database
   createdb coffee_fortune_db
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Run Celery worker (separate terminal)**
   ```bash
   celery -A config worker -l info
   ```

## Redis Protection Features

The `redis_protection.py` module provides:

- **OTP Storage**: Secure temporary storage of OTP codes
- **Rate Limiting**: Prevents OTP request spam (1 request per 60 seconds)
- **Attempt Tracking**: Monitors failed verification attempts
- **Automatic Blocking**: Blocks phone numbers after max failed attempts
- **Configurable Timeouts**: Customizable OTP expiry and block duration

### Configuration

Edit these values in `.env`:

```env
OTP_EXPIRY_SECONDS=300        # OTP valid for 5 minutes
OTP_LENGTH=6                   # 6-digit OTP
MAX_OTP_ATTEMPTS=5            # 5 attempts before blocking
OTP_BLOCK_DURATION=3600       # Block for 1 hour
```

## SMS Provider Integration

The project includes a placeholder for SMS integration in `accounts/tasks.py`. To integrate with your SMS provider:

### Example: Twilio Integration

1. **Install Twilio SDK**
   ```bash
   pip install twilio
   ```

2. **Add to requirements.txt**
   ```
   twilio==8.10.0
   ```

3. **Configure environment variables**
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   ```

4. **Update tasks.py** (uncomment Twilio code block)

### Other SMS Providers

- AWS SNS
- Vonage (Nexmo)
- MessageBird
- Custom SMS gateway

## Security Considerations

### Production Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly (not `CORS_ALLOW_ALL_ORIGINS=True`)
- [ ] Use strong database passwords
- [ ] Enable Redis authentication
- [ ] Set up proper firewall rules
- [ ] Regular security updates
- [ ] Monitor and log authentication attempts

## Testing

### Test OTP Flow (Development Mode)

In DEBUG mode, OTP codes are printed to console/logs:

1. Send OTP request
2. Check Docker logs: `docker-compose logs -f celery`
3. Look for: `[DEBUG MODE] OTP for +1234567890: 123456`
4. Use the OTP to verify

### API Testing with cURL

```bash
# Send OTP
curl -X POST http://localhost:8000/api/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'

# Verify OTP
curl -X POST http://localhost:8000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "otp_code": "123456"}'

# Refresh Token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

## Troubleshooting

### Docker Issues

**Services not starting:**
```bash
docker-compose down -v
docker-compose up -d --build
```

**Database connection errors:**
```bash
# Check if PostgreSQL is healthy
docker-compose ps
docker-compose logs db
```

**Celery not processing tasks:**
```bash
docker-compose logs celery
docker-compose restart celery
```

### Redis Connection Issues

```bash
# Test Redis connection
docker-compose exec redis redis-cli ping
# Should return: PONG
```

### Migration Issues

```bash
# Reset migrations (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

## Contributing

For the Coffee Fortune project team:

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

Proprietary - Coffee Fortune Project

## Support

For issues and questions, contact the development team.
