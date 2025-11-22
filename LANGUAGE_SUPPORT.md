# Language Support Documentation

## Overview
The Coffee Fortune API supports **bilingual responses** in both **English** and **Persian (Farsi)**. Users can request fortune readings in their preferred language, and the AI will respond entirely in that language.

## How It Works

### Language Selection
When creating a new reading, users can specify their preferred language using the `language` parameter:

- `"en"` - English (default)
- `"fa"` - Persian (Farsi)

### API Request Example

#### English Reading
```json
{
  "feature_type": "coffee_fortune",
  "language": "en",
  "image": "<upload image file>"
}
```

#### Persian Reading
```json
{
  "feature_type": "dream_interpretation",
  "language": "fa",
  "text_input": "دیشب خواب دیدم که پرواز می‌کنم"
}
```

### Response Behavior
- When `language: "en"` is selected, the AI responds **entirely in English**
- When `language: "fa"` is selected, the AI responds **entirely in Persian**
- The response is **NOT bilingual** - only the selected language is used

### All Features Support Both Languages
All 10 fortune-telling features support both languages:

1. Coffee Fortune Reading - قهوه فالی
2. Feng Shui Room Analysis - فنگ شویی
3. Dream Interpretation - تعبیر خواب
4. Birthdate Horoscope - طالع بینی تاریخ تولد
5. Tarot Reading - تاروت
6. Numerology Analysis - اعداد شناسی
7. Palm Reading - کف بینی
8. Foot Reading - طالع بینی فرم پا
9. Istikhara - استخاره
10. Geomancy (Ramal) - رمال

### Technical Implementation
The language instruction is automatically added to the AI prompt based on the selected language:

- **English**: No special instruction needed
- **Persian**: Adds instruction to respond in Persian with proper script and cultural sensitivity

## Using the API

### Via Swagger UI
1. Go to http://localhost:8085/api/docs/
2. Navigate to the "Readings" section
3. Click on "POST /api/fortune/readings/"
4. In the request body, set the `language` field to either `"en"` or `"fa"`
5. Fill in other required fields based on the feature type
6. Execute the request

### Via cURL

#### English Example
```bash
curl -X POST "http://localhost:8085/api/fortune/readings/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "tarot",
    "language": "en",
    "text_input": "What does my future hold?"
  }'
```

#### Persian Example
```bash
curl -X POST "http://localhost:8085/api/fortune/readings/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "language": "fa",
    "text_input": "دیشب خواب دیدم که در آسمان پرواز می‌کنم"
  }'
```

## Notes
- The `language` field is optional and defaults to English (`"en"`)
- Persian text input is fully supported
- The AI maintains cultural sensitivity when responding in Persian
- All responses are asynchronous - check the reading status to see when processing is complete
