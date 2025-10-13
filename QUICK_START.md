# Quick Start Guide - Persian Support Enabled 🇮🇷

## 🚀 Start Server in 2 Steps

### Step 1: Run Setup Script
```bash
setup.bat
```
This automatically:
- ✅ Checks Docker
- ✅ Creates `.env` file
- ✅ Builds images
- ✅ Starts services
- ✅ Runs migrations

### Step 2: Load Features
```bash
docker-compose exec web python manage.py populate_features
```

✅ **Server running at:** http://localhost:8000

---

## 🎯 Test Persian Language API

### 1. Get OTP
```bash
curl -X POST http://localhost:8000/api/accounts/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+989123456789"}'
```

### 2. Check OTP in logs
```bash
docker-compose logs celery | findstr OTP
# Find: [DEBUG MODE] OTP for +989123456789: 123456
```

### 3. Verify OTP & Get Token
```bash
curl -X POST http://localhost:8000/api/accounts/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+989123456789", "otp": "123456"}'
```

**Save the access token!**

### 4. Create Reading in Persian 🇮🇷
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "language": "fa",
    "text_input": "خواب دیدم که پرنده‌ای سفید پرواز می‌کند"
  }'
```

### 5. Create Reading in English
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "language": "en",
    "text_input": "I dreamed about flying"
  }'
```

### 6. Check Reading Result
```bash
# Wait 5-10 seconds, then:
curl -X GET http://localhost:8000/api/fortune/readings/READING_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🌐 Language Support

### Supported Languages
- `"en"` - English (default)
- `"fa"` - Persian (Farsi) 🇮🇷

### Usage
Add `"language": "fa"` to any reading request:
```json
{
  "feature_type": "tarot",
  "language": "fa",
  "text_input": "سوال من درباره آینده است"
}
```

**Response will be in Persian:**
```json
{
  "id": "...",
  "language": "fa",
  "interpretation": "تفسیر به زبان فارسی...",
  "status": "completed"
}
```

---

## 🔧 Common Commands

```bash
# View logs
docker-compose logs -f

# Stop server
docker-compose down

# Restart service
docker-compose restart web celery

# Create admin user
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell
```

---

## 🎴 Available Features

All features support both English and Persian!

| Feature | Type | Input | Persian Ready |
|---------|------|-------|---------------|
| Coffee Fortune | `coffee_fortune` | Image | ✅ |
| Feng Shui | `feng_shui` | Image | ✅ |
| Dream Interpretation | `dream_interpretation` | Text | ✅ |
| Birthdate Horoscope | `birthdate_horoscope` | Text | ✅ |
| Tarot Reading | `tarot` | Text | ✅ |
| Numerology | `numerology` | Text | ✅ |
| Palm Reading | `palm_reading` | Image | ✅ |

---

## 🔗 URLs

- **API Base:** http://localhost:8000/api
- **Admin Panel:** http://localhost:8000/admin
- **Auth Endpoints:** http://localhost:8000/api/accounts/
- **Fortune Endpoints:** http://localhost:8000/api/fortune/

---

## 🤖 AI Model Configuration

**Current Model:** `google/gemini-2.0-flash-exp:free`
**Provider:** OpenRouter.ai
**API Key:** ✅ Already configured in `.env`

The Gemini 2.0 Flash model provides:
- ✅ Native Persian language support
- ✅ Cultural context understanding
- ✅ Free tier (via OpenRouter)
- ✅ Fast response times

---

## 📚 Documentation

- **Persian API Guide:** [PERSIAN_API_GUIDE.md](PERSIAN_API_GUIDE.md) - Bilingual guide
- **Full Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md) - Complete setup instructions
- **Changes Summary:** [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) - What's new

---

## ❓ Troubleshooting

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

**Problem:** Persian text shows as ???
- Your terminal/client needs UTF-8 support
- Use Postman or Insomnia for testing

---

## ✅ What's Configured

- ✅ Google Gemini 2.0 Flash model
- ✅ OpenRouter API key
- ✅ Persian (Farsi) language support
- ✅ Docker environment
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Celery background tasks
- ✅ All 7 fortune-telling features

## 🎉 You're Ready!

Start making fortune predictions in **English** and **Persian**!

---

Made with ❤️ for Persian users | ساخته شده با ❤️ برای کاربران فارسی
