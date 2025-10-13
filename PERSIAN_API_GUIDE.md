# Persian Language API Guide
# راهنمای API به زبان فارسی

## Overview | خلاصه

This Coffee Fortune Server now supports Persian (Farsi) language for all fortune-telling interpretations. Simply include `"language": "fa"` in your API requests.

این سرور فال‌گیری قهوه اکنون از زبان فارسی برای تمامی تفسیرها پشتیبانی می‌کند. کافی است `"language": "fa"` را در درخواست‌های API خود قرار دهید.

## Configuration | پیکربندی

### Model Configuration | پیکربندی مدل
- **Model**: `google/gemini-2.0-flash-exp:free`
- **Provider**: OpenRouter.ai
- **Default Model Changed**: Yes, updated from `openai/gpt-4o-mini` to Gemini

### API Key | کلید API
Your API key has been configured in the `.env` file:
```
OPENROUTER_API_KEY=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
```

## API Usage Examples | نمونه‌های استفاده از API

### 1. Coffee Fortune Reading in Persian | فال قهوه به فارسی

```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "feature_type=coffee_fortune" \
  -F "language=fa" \
  -F "image=@/path/to/coffee-cup.jpg"
```

**Response Example:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_phone": "+989123456789",
  "feature": {
    "name": "Coffee Fortune Reading",
    "feature_type": "coffee_fortune",
    "input_type": "image"
  },
  "language": "fa",
  "interpretation": "فال شما نشان می‌دهد که...",
  "status": "completed",
  "model_used": "google/gemini-2.0-flash-exp:free",
  "created_at": "2025-10-12T10:30:00Z"
}
```

### 2. Dream Interpretation in Persian | تعبیر خواب به فارسی

```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "language": "fa",
    "text_input": "دیشب خواب دیدم که..."
  }'
```

### 3. Tarot Reading in Persian | فال تاروت به فارسی

```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "tarot",
    "language": "fa",
    "text_input": "سوال من درباره آینده شغلی است"
  }'
```

### 4. Birthdate Horoscope in Persian | طالع تولد به فارسی

```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "birthdate_horoscope",
    "language": "fa",
    "text_input": "متولد 1370/05/15"
  }'
```

## Supported Features | ویژگی‌های پشتیبانی شده

All features support Persian language:

| Feature Type | English Name | نام فارسی |
|--------------|--------------|-----------|
| `coffee_fortune` | Coffee Fortune Reading | فال قهوه |
| `feng_shui` | Feng Shui Analysis | فنگ شویی |
| `dream_interpretation` | Dream Interpretation | تعبیر خواب |
| `birthdate_horoscope` | Birthdate Horoscope | طالع تولد |
| `tarot` | Tarot Reading | فال تاروت |
| `numerology` | Numerology | اعداد شناسی |
| `palm_reading` | Palm Reading | فال کف دست |

## Language Parameter | پارامتر زبان

### Available Languages | زبان‌های موجود
- `"en"` - English (default)
- `"fa"` - Persian (Farsi)

### Usage | نحوه استفاده
Include the `language` parameter in your request body:
```json
{
  "feature_type": "coffee_fortune",
  "language": "fa",
  "text_input": "متن ورودی"
}
```

If omitted, English will be used by default.
اگر ذکر نشود، به طور پیش‌فرض از انگلیسی استفاده می‌شود.

## Response Format | قالب پاسخ

When `language` is set to `"fa"`, the AI will:
- Respond in Persian script (UTF-8)
- Use culturally appropriate context
- Respect Iranian/Persian traditions
- Format dates and numbers appropriately

زمانی که `language` روی `"fa"` تنظیم شود، هوش مصنوعی:
- به خط فارسی پاسخ می‌دهد (UTF-8)
- از زمینه فرهنگی مناسب استفاده می‌کند
- سنت‌های ایرانی/فارسی را محترم می‌شمارد
- تاریخ‌ها و اعداد را به درستی قالب‌بندی می‌کند

## Character Encoding | کدگذاری کاراکترها

All API responses use UTF-8 encoding. Make sure your client application:
- Supports UTF-8 character encoding
- Can display Persian/Farsi characters
- Handles RTL (Right-to-Left) text properly

تمام پاسخ‌های API از کدگذاری UTF-8 استفاده می‌کنند. اطمینان حاصل کنید برنامه کاربری شما:
- از کدگذاری UTF-8 پشتیبانی می‌کند
- می‌تواند کاراکترهای فارسی را نمایش دهد
- متن راست به چپ (RTL) را به درستی مدیریت می‌کند

## Testing Persian Language | تست زبان فارسی

### Using Python Requests
```python
import requests
import json

url = "http://localhost:8000/api/fortune/readings/"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "feature_type": "dream_interpretation",
    "language": "fa",
    "text_input": "خواب دیدم که پرنده‌ای سفید پرواز می‌کند"
}

response = requests.post(url, headers=headers, json=data)
reading = response.json()
print(reading["interpretation"])
```

### Using JavaScript/Node.js
```javascript
const axios = require('axios');

const url = 'http://localhost:8000/api/fortune/readings/';
const headers = {
  'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
  'Content-Type': 'application/json'
};
const data = {
  feature_type: 'tarot',
  language: 'fa',
  text_input: 'سوال من درباره عشق است'
};

axios.post(url, data, { headers })
  .then(response => {
    console.log(response.data.interpretation);
  });
```

## Common Issues | مشکلات رایج

### Issue: Persian text appears as question marks
**Solution**: Ensure UTF-8 encoding in your client:
```python
# Python
response.encoding = 'utf-8'

# JavaScript
response.setEncoding('utf8');
```

### مشکل: متن فارسی به صورت علامت سوال نمایش داده می‌شود
**راه حل**: از کدگذاری UTF-8 در برنامه خود اطمینان حاصل کنید

### Issue: Text direction is wrong (LTR instead of RTL)
**Solution**: Use CSS for RTL display:
```css
.persian-text {
  direction: rtl;
  text-align: right;
}
```

### مشکل: جهت متن اشتباه است (چپ به راست به جای راست به چپ)
**راه حل**: از CSS برای نمایش RTL استفاده کنید

## Model Behavior | رفتار مدل

The Gemini 2.0 Flash model has been trained on multilingual data including Persian. When instructed to respond in Persian:

مدل Gemini 2.0 Flash روی داده‌های چندزبانه شامل فارسی آموزش دیده است. زمانی که دستور داده شود به فارسی پاسخ دهد:

- **Accuracy**: High accuracy in Persian language understanding
  **دقت**: دقت بالا در درک زبان فارسی

- **Cultural Context**: Understands Iranian/Persian cultural references
  **زمینه فرهنگی**: مراجع فرهنگی ایرانی/فارسی را درک می‌کند

- **Tone**: Can adapt tone for formal/informal Persian
  **لحن**: می‌تواند لحن را برای فارسی رسمی/غیررسمی تنظیم کند

## Deployment Notes | نکات استقرار

### Before Deployment | پیش از استقرار
1. Verify `.env` file contains correct API key
2. Test Persian responses locally
3. Ensure database migrations are applied
4. Check character encoding in production environment

### قبل از استقرار
1. از درستی کلید API در فایل `.env` اطمینان حاصل کنید
2. پاسخ‌های فارسی را به صورت محلی تست کنید
3. اطمینان حاصل کنید مهاجرت‌های پایگاه داده اعمال شده‌اند
4. کدگذاری کاراکترها را در محیط تولید بررسی کنید

## Support | پشتیبانی

For issues related to:
- API functionality: Check application logs
- Persian text rendering: Check client encoding
- Model responses: Verify OpenRouter.ai API key

برای مشکلات مربوط به:
- عملکرد API: لاگ‌های برنامه را بررسی کنید
- نمایش متن فارسی: کدگذاری کلاینت را بررسی کنید
- پاسخ‌های مدل: کلید API از OpenRouter.ai را تأیید کنید

## Contact Information | اطلاعات تماس

- OpenRouter.ai Dashboard: https://openrouter.ai/
- API Documentation: https://openrouter.ai/docs
- Model Information: https://openrouter.ai/models/google/gemini-2.0-flash-exp

---

Made with ❤️ for Persian users | ساخته شده با ❤️ برای کاربران فارسی
