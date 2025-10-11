# Coffee Fortune Server - API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

The API uses JWT (JSON Web Token) authentication with OTP-based phone number verification.

### Flow Overview

1. User requests OTP by providing phone number
2. OTP is sent via SMS (handled by Celery worker)
3. User submits OTP for verification
4. Server returns JWT access and refresh tokens
5. Client uses access token for authenticated requests
6. Client refreshes token when access token expires

---

## Endpoints

### 1. Send OTP

Send an OTP code to a phone number.

**Endpoint:** `POST /api/auth/send-otp/`

**Authentication:** Not required

**Rate Limiting:**
- 1 request per 60 seconds per phone number
- Blocked after 5 failed verification attempts (1 hour block)

**Request Body:**
```json
{
    "phone_number": "+1234567890"
}
```

**Success Response (200 OK):**
```json
{
    "message": "OTP sent successfully",
    "phone_number": "+1234567890",
    "expires_in": 300
}
```

**Error Responses:**

**400 Bad Request** - Invalid phone number:
```json
{
    "error": {
        "phone_number": ["Invalid phone number format"]
    }
}
```

**429 Too Many Requests** - Rate limit exceeded:
```json
{
    "error": "Please wait before requesting another OTP"
}
```

**429 Too Many Requests** - Phone number blocked:
```json
{
    "error": "Too many failed attempts. Please try again later."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

---

### 2. Verify OTP

Verify the OTP code and receive JWT tokens.

**Endpoint:** `POST /api/auth/verify/`

**Authentication:** Not required

**Request Body:**
```json
{
    "phone_number": "+1234567890",
    "otp_code": "123456"
}
```

**Success Response (200 OK):**
```json
{
    "message": "Authentication successful",
    "user": {
        "id": 1,
        "phone_number": "+1234567890",
        "first_name": "",
        "last_name": "",
        "date_joined": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-01T12:00:00Z"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

**Error Responses:**

**400 Bad Request** - Invalid OTP:
```json
{
    "error": "Invalid OTP code",
    "remaining_attempts": 3
}
```

**400 Bad Request** - OTP expired:
```json
{
    "error": "OTP expired or not found. Please request a new one."
}
```

**400 Bad Request** - Validation error:
```json
{
    "error": {
        "otp_code": ["Ensure this field has at least 6 characters."]
    }
}
```

**429 Too Many Requests** - Too many failed attempts:
```json
{
    "error": "Too many failed attempts. Your phone number has been temporarily blocked."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "otp_code": "123456"
  }'
```

---

### 3. Refresh Token

Get a new access token using the refresh token.

**Endpoint:** `POST /api/auth/token/refresh/`

**Authentication:** Not required (uses refresh token)

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response:**

**401 Unauthorized** - Invalid or expired refresh token:
```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

---

## Using Access Tokens

Once you have an access token, include it in the `Authorization` header for authenticated requests:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Example:**
```bash
curl -X GET http://localhost:8000/api/some-protected-endpoint/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## Token Lifetimes

- **Access Token:** 24 hours
- **Refresh Token:** 30 days
- **OTP Code:** 5 minutes (300 seconds)

---

## Security Features

### Brute-Force Protection

- **Rate Limiting:** Maximum 1 OTP request per 60 seconds per phone number
- **Attempt Tracking:** System tracks failed OTP verification attempts
- **Auto-Blocking:** After 5 failed verification attempts, phone number is blocked for 1 hour
- **OTP Expiry:** OTP codes expire after 5 minutes

### Configuration

These values can be adjusted in the `.env` file:

```env
OTP_EXPIRY_SECONDS=300      # 5 minutes
OTP_LENGTH=6                 # 6-digit OTP
MAX_OTP_ATTEMPTS=5          # 5 attempts before blocking
OTP_BLOCK_DURATION=3600     # 1 hour block
```

---

## Error Handling

All error responses follow this format:

```json
{
    "error": "Error message here"
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

### Common HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid input or validation error
- `401 Unauthorized` - Invalid or missing authentication token
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## Testing in Development Mode

When `DEBUG=True`, OTP codes are logged to the console and Celery worker logs.

**View OTP codes:**
```bash
docker-compose logs -f celery
```

You'll see output like:
```
[DEBUG MODE] OTP for +1234567890: 123456
```

---

## Android Integration Example

### Kotlin Example using Retrofit

```kotlin
// API Service Interface
interface CoffeeFortuneApi {

    @POST("auth/send-otp/")
    suspend fun sendOtp(@Body request: SendOtpRequest): Response<SendOtpResponse>

    @POST("auth/verify/")
    suspend fun verifyOtp(@Body request: VerifyOtpRequest): Response<VerifyOtpResponse>

    @POST("auth/token/refresh/")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<RefreshTokenResponse>
}

// Data Classes
data class SendOtpRequest(val phone_number: String)
data class SendOtpResponse(
    val message: String,
    val phone_number: String,
    val expires_in: Int
)

data class VerifyOtpRequest(
    val phone_number: String,
    val otp_code: String
)

data class VerifyOtpResponse(
    val message: String,
    val user: User,
    val tokens: Tokens
)

data class User(
    val id: Int,
    val phone_number: String,
    val first_name: String,
    val last_name: String
)

data class Tokens(
    val refresh: String,
    val access: String
)

// Usage Example
class AuthRepository(private val api: CoffeeFortuneApi) {

    suspend fun sendOtp(phoneNumber: String): Result<SendOtpResponse> {
        return try {
            val response = api.sendOtp(SendOtpRequest(phoneNumber))
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to send OTP"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun verifyOtp(phoneNumber: String, otpCode: String): Result<VerifyOtpResponse> {
        return try {
            val response = api.verifyOtp(VerifyOtpRequest(phoneNumber, otpCode))
            if (response.isSuccessful) {
                // Store tokens securely
                val tokens = response.body()!!.tokens
                storeTokens(tokens)
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Invalid OTP"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun storeTokens(tokens: Tokens) {
        // Store tokens in SharedPreferences or DataStore
        // Implementation depends on your app architecture
    }
}
```

---

## Support

For questions or issues, contact the development team.

**Last Updated:** January 2025
