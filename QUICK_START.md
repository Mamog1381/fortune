# Quick Start Guide

## Start Server (5 minutes)

```bash
# 1. Start services
docker-compose up -d --build

# 2. Initialize database
docker-compose exec web python manage.py migrate

# 3. Load fortune features
docker-compose exec web python manage.py populate_features

# 4. Check status
docker-compose exec web python manage.py check_api_status
```

✅ **Server running at:** http://localhost:8000

---

## Test API

### 1. Get OTP
```bash
curl -X POST http://localhost:8000/api/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

### 2. Check OTP in logs
```bash
docker-compose logs -f celery
# Find: [DEBUG MODE] OTP for +1234567890: 123456
```

### 3. Verify OTP & Get Token
```bash
curl -X POST http://localhost:8000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "otp_code": "123456"}'
```

**Save the access token!**

### 4. List Fortune Features
```bash
curl -X GET http://localhost:8000/api/fortune/features/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Create Reading (Text)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "text_input": "I dreamed about flying"
  }'
```

### 6. Check Reading Result
```bash
# Wait 3-5 seconds, then:
curl -X GET http://localhost:8000/api/fortune/readings/READING_ID/status_check/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop server
docker-compose down

# Restart service
docker-compose restart web

# Create admin user
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell
```

---

## Available Features

| Feature | Type | Input |
|---------|------|-------|
| Coffee Fortune | `coffee_fortune` | Image |
| Feng Shui | `feng_shui` | Image |
| Dream Interpretation | `dream_interpretation` | Text |
| Birthdate Horoscope | `birthdate_horoscope` | Text |
| Tarot Reading | `tarot` | Text |
| Numerology | `numerology` | Text |
| Palm Reading | `palm_reading` | Image |

---

## URLs

- **API Base:** http://localhost:8000/api
- **Admin Panel:** http://localhost:8000/admin
- **Auth Endpoints:** http://localhost:8000/api/auth/
- **Fortune Endpoints:** http://localhost:8000/api/fortune/

---

## Add OpenRouter API Key

1. Get key: https://openrouter.ai/keys
2. Edit `.env` file: `OPENROUTER_API_KEY=your-key-here`
3. Restart: `docker-compose restart web celery`

**Without key:** System runs in MOCK MODE (perfect for testing!)

---

## Troubleshooting

**Problem:** Database error
```bash
docker-compose restart db
docker-compose exec web python manage.py migrate
```

**Problem:** Celery not working
```bash
docker-compose restart celery
docker-compose logs celery
```

**Problem:** No features
```bash
docker-compose exec web python manage.py populate_features
```

---

## Full Documentation

- 📖 [Deployment Guide](DEPLOYMENT_GUIDE.md)
- 🔐 [Auth API](API_DOCUMENTATION.md)
- 🔮 [Fortune API](FORTUNE_API_DOCUMENTATION.md)
- 📝 [Main README](README.md)
