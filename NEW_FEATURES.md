# New Features Added - 3 Additional Fortune Telling Services
# فیچرهای جدید - 3 سرویس فال‌بینی اضافی

## Summary | خلاصه

3 new fortune-telling features have been added to the Coffee Fortune Server:

سه فیچر جدید فال‌بینی به سرور اضافه شده است:

1. **Foot Reading** - طالع بینی فرم پا (Image-based)
2. **Istikhara** - استخاره (Text-based)
3. **Geomancy (Ramal)** - رمال (Text-based)

---

## 1. Foot Reading / طالع بینی فرم پا

### Description
An ancient practice of reading personality, life path, and destiny through foot characteristics, lines, and patterns.

### توضیحات فارسی
یک روش کهن برای خواندن شخصیت، مسیر زندگی و سرنوشت از طریق ویژگی‌ها، خطوط و الگوهای پا.

### API Details
- **Feature Type**: `foot_reading`
- **Input Type**: `image` (Photo of foot)
- **Language Support**: English (`en`) & Persian (`fa`)
- **Credit Cost**: 2 credits

### Example Request
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "feature_type=foot_reading" \
  -F "language=fa" \
  -F "image=@/path/to/foot-photo.jpg"
```

### What It Analyzes
- **Foot Shape & Type**: Overall shape and personality indicators
- **Toe Analysis**: Each toe's meaning (leadership, communication, career, love, adaptability)
- **Sole Lines & Patterns**: Life line, heart line, head line, fate line
- **Arch Analysis**: High, medium, or flat arch significance
- **Skin Texture & Color**: Health and energy indicators
- **Personality Insights**: Temperament, emotional patterns, decision-making
- **Life Path**: Journey and destiny insights
- **Health Indicators**: Physical and energetic wellness
- **Strengths & Talents**: Natural abilities
- **Guidance**: Practical advice

### تحلیل‌های انجام شده
- شکل و نوع پا
- تحلیل انگشتان پا
- خطوط کف پا
- تحلیل قوس پا
- بافت و رنگ پوست
- بینش شخصیتی
- مسیر زندگی
- شاخص‌های سلامت
- نقاط قوت و استعداد
- راهنمایی عملی

---

## 2. Istikhara / استخاره

### Description
Spiritual guidance consultation based on Islamic tradition of seeking divine direction for important decisions.

### توضیحات فارسی
مشاوره راهنمایی معنوی بر اساس سنت اسلامی برای دریافت راهنمایی الهی در تصمیمات مهم.

### API Details
- **Feature Type**: `istikhara`
- **Input Type**: `text` (Your question or dilemma)
- **Language Support**: English (`en`) & Persian (`fa`)
- **Credit Cost**: 1 credit

### Example Request (Persian)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "istikhara",
    "language": "fa",
    "text_input": "آیا باید شغلم را تغییر بدهم؟"
  }'
```

### Example Request (English)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "istikhara",
    "language": "en",
    "text_input": "Should I change my job?"
  }'
```

### What It Provides
- **Understanding**: Deep reflection on your question
- **Spiritual Perspective**: Divine wisdom viewpoint
- **Signs & Intuition**: Spiritual insights
- **Path Analysis**: Positive outcomes and challenges
- **Heart Wisdom**: Inner knowing guidance
- **Practical Spiritual Advice**: Prayers and contemplation
- **Inner Peace Guidance**: Finding tranquility
- **Trust & Surrender**: Divine timing wisdom
- **Reflection Questions**: Connect with inner wisdom
- **Final Guidance**: Hope, faith, and support

### موارد ارائه شده
- درک عمیق سوال
- دیدگاه معنوی
- نشانه‌ها و شهود
- تحلیل مسیرها
- حکمت قلبی
- مشاوره معنوی عملی
- راهنمایی آرامش درونی
- توکل و تسلیم
- سوالات تأملی
- راهنمایی نهایی

---

## 3. Geomancy (Ramal) / رمال

### Description
Ancient Arabic/Islamic divination system using geomantic figures and patterns to answer questions and reveal hidden knowledge.

### توضیحات فارسی
سیستم فال‌بینی کهن عربی/اسلامی که از اشکال و الگوهای رملی برای پاسخ به سوالات و آشکار کردن دانش پنهان استفاده می‌کند.

### API Details
- **Feature Type**: `ramal`
- **Input Type**: `text` (Your question)
- **Language Support**: English (`en`) & Persian (`fa`)
- **Credit Cost**: 2 credits

### Example Request (Persian)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "ramal",
    "language": "fa",
    "text_input": "آینده عشقی من چگونه خواهد بود؟"
  }'
```

### Example Request (English)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "ramal",
    "language": "en",
    "text_input": "What does my future hold in love?"
  }'
```

### What It Provides
- **Geomantic Figures**: Four Mother figures cast for your question
- **The Geomantic Shield**: Complete shield with all 15 figures
  - Mother figures (4)
  - Daughter figures (4)
  - Niece figures (4)
  - Witness figures (2)
  - Judge figure (1)
- **Figure Meanings**: Traditional interpretations
- **Elemental Associations**: Earth, Air, Fire, Water
- **Planetary Rulers**: Astrological connections
- **House Analysis**: Question through astrological houses
- **Time Frame**: When outcomes may manifest
- **Obstacles & Opportunities**: Challenges and favorable conditions
- **Overall Reading**: Direct answer with insights
- **Practical Guidance**: Actions to take
- **Spiritual Message**: Deeper esoteric wisdom

### موارد ارائه شده
- اشکال رملی (16 شکل اصلی)
- سپر رملی کامل
- معانی سنتی اشکال
- ارتباطات عنصری
- حاکمان سیاره‌ای
- تحلیل خانه‌های نجومی
- بازه زمانی
- موانع و فرصت‌ها
- فال کامل
- راهنمایی عملی
- پیام معنوی

---

## Complete Feature List | لیست کامل فیچرها

Now the system has **10 fortune-telling features**:

اکنون سیستم دارای **10 فیچر فال‌بینی** است:

| # | Feature Type | English Name | نام فارسی | Input Type | Credits |
|---|--------------|--------------|-----------|------------|---------|
| 1 | `coffee_fortune` | Coffee Fortune Reading | فال قهوه | Image | 2 |
| 2 | `feng_shui` | Feng Shui Room Analysis | فنگ شویی | Image | 2 |
| 3 | `dream_interpretation` | Dream Interpretation | تعبیر خواب | Text | 1 |
| 4 | `birthdate_horoscope` | Birthdate Horoscope | طالع تولد | Text | 1 |
| 5 | `tarot` | Tarot Reading | فال تاروت | Text | 1 |
| 6 | `numerology` | Numerology Analysis | اعداد شناسی | Text | 2 |
| 7 | `palm_reading` | Palm Reading | فال کف دست | Image | 2 |
| 8 | `foot_reading` | **Foot Reading** | **طالع بینی فرم پا** | Image | 2 |
| 9 | `istikhara` | **Istikhara** | **استخاره** | Text | 1 |
| 10 | `ramal` | **Geomancy (Ramal)** | **رمال** | Text | 2 |

---

## Deployment Steps | مراحل استقرار

### Step 1: Apply Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Step 2: Load New Features
```bash
docker-compose exec web python manage.py populate_features
```

This will:
- Update all existing features to use Gemini model
- Add 3 new features (foot_reading, istikhara, ramal)

### Step 3: Verify Features
```bash
# List all features via API
curl -X GET http://localhost:8000/api/fortune/features/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

You should see 10 features total.

---

## Testing New Features | تست فیچرهای جدید

### Test 1: Foot Reading (Persian)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "feature_type=foot_reading" \
  -F "language=fa" \
  -F "image=@foot.jpg"
```

### Test 2: Istikhara (Persian)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "istikhara",
    "language": "fa",
    "text_input": "آیا باید این پیشنهاد را بپذیرم؟"
  }'
```

### Test 3: Ramal (Persian)
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "ramal",
    "language": "fa",
    "text_input": "آینده شغلی من چگونه است؟"
  }'
```

---

## AI Model Configuration | پیکربندی مدل هوش مصنوعی

All features now use:
- **Model**: `google/gemini-2.0-flash-exp:free`
- **Provider**: OpenRouter.ai
- **Benefits**:
  - ✅ Free tier
  - ✅ Excellent Persian language support
  - ✅ Cultural context understanding
  - ✅ Fast response times
  - ✅ High token limits

---

## Image Requirements | الزامات تصویر

For image-based features (coffee_fortune, feng_shui, palm_reading, **foot_reading**):

### Recommended
- **Format**: JPG, PNG
- **Size**: Max 10MB
- **Resolution**: At least 800x600 pixels
- **Quality**: Clear, well-lit photos
- **Angle**: Direct, straight-on view

### برای عکس پا (Foot Reading)
- عکس واضح و با نور کافی
- نمای مستقیم از کف پا
- تمام انگشتان پا باید واضح باشند
- پس‌زمینه ساده و روشن

---

## Cultural Sensitivity | حساسیت فرهنگی

The new features have been designed with cultural sensitivity:

### Istikhara | استخاره
- Respects Islamic traditions
- Emphasizes divine guidance
- No definitive predictions (guidance only)
- Encourages prayer and contemplation

### Ramal | رمال
- Uses authentic geomantic practices
- Traditional figure names and meanings
- Respects Middle Eastern/Islamic heritage
- Combines mystical and practical wisdom

### Foot Reading | طالع بینی فرم پا
- Acknowledges ancient wisdom traditions
- Respectful of cultural practices
- Provides both mystical and practical insights

---

## Troubleshooting | عیب‌یابی

### Issue: Features not appearing
```bash
# Re-run populate command
docker-compose exec web python manage.py populate_features
```

### Issue: Old model still being used
```bash
# Update all features manually
docker-compose exec web python manage.py shell
```
```python
from fortune.models import FortuneFeature
FortuneFeature.objects.all().update(model_name='google/gemini-2.0-flash-exp:free')
```

### Issue: Persian responses not showing
- Check language parameter: `"language": "fa"`
- Ensure UTF-8 encoding in client
- Verify OpenRouter API key is set

---

## Credits & Pricing | اعتبار و قیمت‌گذاری

| Feature | Credits | Value |
|---------|---------|-------|
| Text-based readings | 1 credit | Simple |
| Image-based readings | 2 credits | Complex |

**New Features**:
- Foot Reading: 2 credits (image analysis)
- Istikhara: 1 credit (spiritual guidance)
- Ramal: 2 credits (complex geomantic calculation)

---

## Support | پشتیبانی

For more information:
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Persian Guide**: [PERSIAN_API_GUIDE.md](PERSIAN_API_GUIDE.md)
- **Full Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Version**: 2.1 with 3 new features
**Date**: 2025-10-12
**Total Features**: 10 fortune-telling services

Made with ❤️ for Persian and international users
ساخته شده با ❤️ برای کاربران ایرانی و بین‌المللی
