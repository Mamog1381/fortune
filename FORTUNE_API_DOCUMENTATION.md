# Fortune Features API Documentation

## Base URL
```
http://localhost:8000/api/fortune
```

## Authentication

All fortune endpoints require JWT authentication. Include the access token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

---

## Endpoints Overview

1. **GET /api/fortune/features/** - List all available fortune features
2. **GET /api/fortune/features/{id}/** - Get specific feature details
3. **GET /api/fortune/features/by_type/?type={feature_type}** - Get feature by type
4. **POST /api/fortune/readings/** - Create a new reading
5. **GET /api/fortune/readings/** - List user's readings
6. **GET /api/fortune/readings/{id}/** - Get specific reading
7. **GET /api/fortune/readings/recent/?limit=10** - Get recent readings
8. **GET /api/fortune/readings/{id}/status_check/** - Check reading status
9. **POST /api/fortune/readings/{id}/feedback/** - Submit feedback
10. **GET /api/fortune/history/** - View reading history
11. **GET /api/fortune/history/statistics/** - Get usage statistics

---

## 1. List Fortune Features

Get all available fortune-telling features.

**Endpoint:** `GET /api/fortune/features/`

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Coffee Fortune Reading",
      "feature_type": "coffee_fortune",
      "input_type": "image",
      "description": "Upload a photo of your coffee cup and receive a mystical fortune reading based on the patterns in your coffee grounds.",
      "credit_cost": 2,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "name": "Dream Interpretation",
      "feature_type": "dream_interpretation",
      "input_type": "text",
      "description": "Share your dream and receive an in-depth interpretation revealing hidden meanings and insights.",
      "credit_cost": 1,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/fortune/features/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

## 2. Get Feature by Type

Get a specific feature by its type identifier.

**Endpoint:** `GET /api/fortune/features/by_type/?type={feature_type}`

**Authentication:** Required

**Query Parameters:**
- `type` (required): Feature type identifier

**Available Feature Types:**
- `coffee_fortune` - Coffee Fortune Reading (image)
- `feng_shui` - Feng Shui Room Analysis (image)
- `dream_interpretation` - Dream Interpretation (text)
- `birthdate_horoscope` - Birthdate Horoscope (text)
- `tarot` - Tarot Reading (text)
- `numerology` - Numerology Analysis (text)
- `palm_reading` - Palm Reading (image)

**Success Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Coffee Fortune Reading",
  "feature_type": "coffee_fortune",
  "input_type": "image",
  "description": "Upload a photo of your coffee cup...",
  "credit_cost": 2,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/fortune/features/by_type/?type=coffee_fortune" \
  -H "Authorization: Bearer <your_access_token>"
```

---

## 3. Create a Reading

Submit a new fortune reading request.

**Endpoint:** `POST /api/fortune/readings/`

**Authentication:** Required

**Content-Type:**
- For text-only: `application/json`
- For image uploads: `multipart/form-data`

### Text-Based Reading (Dream, Horoscope, Tarot, etc.)

**Request Body (JSON):**
```json
{
  "feature_type": "dream_interpretation",
  "text_input": "I dreamed I was flying over a vast ocean, and suddenly I saw a lighthouse in the distance. The light was very bright and comforting."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "text_input": "Your dream description here..."
  }'
```

### Image-Based Reading (Coffee Fortune, Feng Shui, Palm Reading)

**Request Body (multipart/form-data):**
- `feature_type`: string (required) - e.g., "coffee_fortune"
- `image`: file (required) - JPG, PNG, or WEBP format, max 10MB

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer <your_access_token>" \
  -F "feature_type=coffee_fortune" \
  -F "image=@/path/to/coffee_cup.jpg"
```

### Success Response (201 Created):
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174002",
  "user_phone": "+1234567890",
  "feature": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Coffee Fortune Reading",
    "feature_type": "coffee_fortune",
    "input_type": "image",
    "description": "Upload a photo of your coffee cup...",
    "credit_cost": 2,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "text_input": null,
  "image": "http://localhost:8000/media/readings/2024/01/15/coffee_cup.jpg",
  "interpretation": null,
  "status": "pending",
  "error_message": null,
  "model_used": null,
  "tokens_used": 0,
  "processing_time": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Note:** The reading is processed asynchronously. The status will be `pending` initially, then `processing`, and finally `completed` or `failed`. Poll the status or retrieve the reading later to get the interpretation.

---

## 4. Check Reading Status

Check if a reading has been completed.

**Endpoint:** `GET /api/fortune/readings/{id}/status_check/`

**Authentication:** Required

**Success Response (200 OK) - Processing:**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174002",
  "status": "processing",
  "interpretation": null,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Success Response (200 OK) - Completed:**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174002",
  "user_phone": "+1234567890",
  "feature": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Coffee Fortune Reading",
    "feature_type": "coffee_fortune"
  },
  "interpretation": "🔮 Your Coffee Fortune Reading...\n\n**What I See:**\nIn the patterns of your coffee grounds, I observe several significant symbols...",
  "status": "completed",
  "model_used": "openai/gpt-4o-mini",
  "tokens_used": 856,
  "processing_time": 3.45,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:05Z"
}
```

---

## 5. List User's Readings

Get all readings for the authenticated user with optional filtering.

**Endpoint:** `GET /api/fortune/readings/`

**Authentication:** Required

**Query Parameters (optional):**
- `status`: Filter by status (pending, processing, completed, failed)
- `feature__feature_type`: Filter by feature type
- `page`: Page number for pagination

**Success Response (200 OK):**
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/fortune/readings/?page=2",
  "previous": null,
  "results": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174002",
      "user_phone": "+1234567890",
      "feature": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Coffee Fortune Reading",
        "feature_type": "coffee_fortune"
      },
      "status": "completed",
      "interpretation": "Your fortune reading...",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Example cURL:**
```bash
# Get all completed readings
curl -X GET "http://localhost:8000/api/fortune/readings/?status=completed" \
  -H "Authorization: Bearer <your_access_token>"

# Get all dream interpretations
curl -X GET "http://localhost:8000/api/fortune/readings/?feature__feature_type=dream_interpretation" \
  -H "Authorization: Bearer <your_access_token>"
```

---

## 6. Get Recent Readings

Get the most recent readings for the user.

**Endpoint:** `GET /api/fortune/readings/recent/?limit={number}`

**Authentication:** Required

**Query Parameters:**
- `limit` (optional): Number of readings to return (default: 10)

**Success Response (200 OK):**
```json
[
  {
    "id": "456e7890-e89b-12d3-a456-426614174002",
    "feature": {
      "name": "Coffee Fortune Reading",
      "feature_type": "coffee_fortune"
    },
    "status": "completed",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## 7. Submit Feedback

Rate and provide feedback for a completed reading.

**Endpoint:** `POST /api/fortune/readings/{id}/feedback/`

**Authentication:** Required

**Request Body:**
```json
{
  "rating": 5,
  "feedback": "This reading was incredibly accurate and insightful!"
}
```

**Fields:**
- `rating` (required): Integer from 1 to 5
- `feedback` (optional): Text feedback

**Success Response (200 OK):**
```json
{
  "message": "Feedback submitted successfully",
  "rating": 5
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Can only provide feedback for completed readings"
}
```

---

## 8. View Reading History

Get reading history with feedback.

**Endpoint:** `GET /api/fortune/history/`

**Authentication:** Required

**Query Parameters (optional):**
- `feature__feature_type`: Filter by feature type
- `rating`: Filter by rating (1-5)

**Success Response (200 OK):**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "feature": {
        "name": "Coffee Fortune Reading",
        "feature_type": "coffee_fortune"
      },
      "reading": {
        "id": "456e7890-e89b-12d3-a456-426614174002",
        "interpretation": "Your fortune...",
        "status": "completed"
      },
      "rating": 5,
      "feedback": "Amazing!",
      "created_at": "2024-01-15T10:35:00Z"
    }
  ]
}
```

---

## 9. Get Usage Statistics

Get statistics about the user's fortune reading usage.

**Endpoint:** `GET /api/fortune/history/statistics/`

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "total_readings": 25,
  "features_used": 5,
  "average_rating": 4.6,
  "most_used_feature": "Dream Interpretation",
  "most_used_count": 10
}
```

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Reading created successfully
- `400 Bad Request` - Invalid input or validation error
- `401 Unauthorized` - Authentication required or token invalid
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message description"
}
```

Or for validation errors:

```json
{
  "error": {
    "field_name": ["Error message for this field"]
  }
}
```

---

## Image Requirements

For image-based features (Coffee Fortune, Feng Shui, Palm Reading):

- **Supported formats:** JPG, JPEG, PNG, WEBP
- **Maximum size:** 10 MB
- **Recommended:** Clear, well-lit photos for best results

---

## Processing Time

- Text-based readings: Typically 2-5 seconds
- Image-based readings: Typically 5-10 seconds

Readings are processed asynchronously using Celery workers. You can:
1. Poll the status endpoint periodically
2. Retrieve the reading later from your readings list

---

## Mock Mode

If the OpenRouter API key is not configured, the system operates in **MOCK MODE**:

- All features remain functional
- Readings return demonstration responses
- No actual AI processing occurs
- Useful for frontend development and testing

To enable real AI-powered readings, configure `OPENROUTER_API_KEY` in your `.env` file.

---

## Complete Workflow Example

### 1. Get Available Features
```bash
curl -X GET http://localhost:8000/api/fortune/features/ \
  -H "Authorization: Bearer <token>"
```

### 2. Create a Reading
```bash
curl -X POST http://localhost:8000/api/fortune/readings/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_type": "dream_interpretation",
    "text_input": "I dreamed about flying..."
  }'
```

### 3. Check Status (wait a few seconds)
```bash
curl -X GET http://localhost:8000/api/fortune/readings/{reading_id}/status_check/ \
  -H "Authorization: Bearer <token>"
```

### 4. Submit Feedback
```bash
curl -X POST http://localhost:8000/api/fortune/readings/{reading_id}/feedback/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "feedback": "Great reading!"
  }'
```

---

## Rate Limiting

Currently no rate limiting on fortune features. Consider implementing based on:
- Credit system (already in place per feature)
- Per-user daily limits
- Per-feature cooldowns

---

**Last Updated:** January 2025
