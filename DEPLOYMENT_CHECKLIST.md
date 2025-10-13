# 🚀 چک لیست دیپلوی روی VPS

این چک لیست قدم به قدم به شما کمک می‌کند تا پروژه را آماده دیپلوی کنید.

---

## 📋 بخش 1: اطلاعات پایه (قبل از شروع)

### اطلاعات VPS
- [ ] **آی‌پی VPS**: `_________________`
- [ ] **Username**: `_________________`
- [ ] **سیستم عامل**: Ubuntu 20.04/22.04
- [ ] **RAM**: حداقل 2GB (4GB توصیه می‌شود)

### اطلاعات دامنه (اختیاری اما توصیه می‌شود)
- [ ] **نام دامنه**: `_________________`
- [ ] **DNS تنظیم شده**: A Record به IP سرور اشاره کند
- [ ] **زمان propagation**: معمولاً 1-24 ساعت

---

## 🔧 بخش 2: فایل .env - مقداردهی متغیرهای محیطی

### ✅ چیزایی که حتماً باید تغییر بدی:

#### 1. Django Settings
```bash
SECRET_KEY=______________________ # ⚠️ CRITICAL - حتماً تولید کن
DEBUG=False                       # ⚠️ CRITICAL - حتما False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,YOUR_VPS_IP
```

**نحوه تولید SECRET_KEY:**
```bash
# روی کامپیوتر محلی یا VPS اجرا کن:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### 2. Database Configuration
```bash
DATABASE_URL=postgresql://postgres:CHANGE_THIS_PASSWORD@db:5432/coffee_fortune_db
```
**⚠️ CRITICAL**: پسورد دیتابیس رو حتماً تغییر بده!
- پسورد قوی انتخاب کن (حداقل 16 کاراکتر)
- از ترکیب حروف، اعداد و کاراکترهای خاص استفاده کن

#### 3. OpenRouter API Key
```bash
OPENROUTER_API_KEY=sk-or-v1-____________________ # ⚠️ CRITICAL
```
**کجا بگیرم؟** https://openrouter.ai/keys
- اکانت بساز
- کلید API جدید بساز
- کلید رو اینجا کپی کن

#### 4. CORS Configuration
```bash
CORS_ALLOW_ALL_ORIGINS=False      # ⚠️ CRITICAL - حتما False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```
**توضیح**: دامنه فرانت‌اند خودت رو اینجا بنویس (با https://)

---

### ⚡ چیزایی که می‌تونی بعداً تغییر بدی:

#### 5. OTP Configuration (برای SMS)
```bash
OTP_EXPIRY_SECONDS=120            # مدت اعتبار کد یکبار مصرف (ثانیه)
SMS_API_KEY=______________________
```
**الان اجباری نیست** - فعلاً برای تست می‌تونی خالی بذاری

#### 6. Email Configuration (اختیاری)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
**الان اجباری نیست** - برای نوتیفیکیشن‌های ایمیلی

---

### 🔒 Security Settings (فعال می‌شه وقتی DEBUG=False)
این تنظیمات به صورت اتوماتیک فعال می‌شن، نیازی به تغییر نیست:
```bash
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

## 📝 بخش 3: فایل‌های دیگه که باید چک کنی

### 1. docker-compose.prod.yml
```yaml
# خط 15: پسورد دیتابیس
- POSTGRES_PASSWORD=${DB_PASSWORD}
```
**باید اضافه کنی به .env:**
```bash
DB_PASSWORD=YOUR_STRONG_DATABASE_PASSWORD
```

### 2. nginx/nginx.conf
```nginx
# خط 7 و 55: اگه دامنه داری
server_name yourdomain.com www.yourdomain.com;

# خط 59-60: بعد از گرفتن SSL (مرحله بعد)
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

---

## 🎯 بخش 4: خلاصه چیزایی که باید حتماً مقداردهی کنی

### ✅ فایل .env روی VPS:

```env
# ===== CRITICAL - باید حتماً تغییر بدی =====
SECRET_KEY=<تولید_کن_با_دستور_بالا>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,YOUR_VPS_IP
DATABASE_URL=postgresql://postgres:<پسورد_قوی>@db:5432/coffee_fortune_db
DB_PASSWORD=<همون_پسورد_بالا>
OPENROUTER_API_KEY=sk-or-v1-<کلید_API_از_OpenRouter>
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# ===== اختیاری - می‌تونی بعداً اضافه کنی =====
SMS_API_KEY=<برای_ارسال_OTP>
EMAIL_HOST_USER=<برای_ارسال_ایمیل>
EMAIL_HOST_PASSWORD=<برای_ارسال_ایمیل>

# ===== می‌تونی همینطوری بمونن =====
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
OTP_EXPIRY_SECONDS=120
```

---

## 🚀 بخش 5: مراحل دیپلوی (قدم به قدم)

### مرحله 1: آماده‌سازی VPS
```bash
# وصل شو به VPS
ssh root@YOUR_VPS_IP

# آپدیت سیستم
sudo apt update && sudo apt upgrade -y

# نصب Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# نصب Docker Compose
sudo apt install docker-compose -y

# نصب Git
sudo apt install git -y

# فایروال
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### مرحله 2: کلون پروژه
```bash
cd /home/$USER
git clone <آدرس_ریپوی_شما> coffee-fortune-server
cd coffee-fortune-server
```

### مرحله 3: ساخت فایل .env
```bash
# کپی از نمونه
cp .env.production.example .env

# ویرایش
nano .env

# مقادیر بالا رو پر کن و ذخیره کن (Ctrl+X, Y, Enter)
```

### مرحله 4: بیلد و اجرا
```bash
# بیلد
docker-compose -f docker-compose.prod.yml build

# اجرا
docker-compose -f docker-compose.prod.yml up -d

# چک کن همه سرویس‌ها running باشن
docker-compose -f docker-compose.prod.yml ps
```

### مرحله 5: مایگریشن و setup
```bash
# مایگریشن دیتابیس
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# جمع‌آوری فایل‌های استاتیک
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# ساخت superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# پر کردن features
docker-compose -f docker-compose.prod.yml exec web python manage.py populate_features
```

### مرحله 6: تست
```bash
# تست health endpoint
curl http://YOUR_VPS_IP/health

# تست API
curl http://YOUR_VPS_IP/api/fortune/features/
```

### مرحله 7: SSL Certificate (اختیاری اما توصیه می‌شود)
```bash
# نصب Certbot
sudo apt install certbot -y

# توقف موقت nginx
docker-compose -f docker-compose.prod.yml stop nginx

# دریافت گواهی
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# ویرایش nginx config
nano nginx/nginx.conf
# خط 7: server_name yourdomain.com www.yourdomain.com;
# uncomment کن server block دوم (HTTPS)
# uncomment کن خط 11: return 301 https://...

# ویرایش docker-compose.prod.yml
nano docker-compose.prod.yml
# uncomment کن خط 99: - /etc/letsencrypt:/etc/letsencrypt:ro

# restart nginx
docker-compose -f docker-compose.prod.yml up -d nginx

# تست HTTPS
curl https://yourdomain.com/health
```

---

## ✅ چک لیست نهایی

### قبل از دیپلوی:
- [ ] SECRET_KEY جدید تولید کردم
- [ ] DEBUG=False گذاشتم
- [ ] ALLOWED_HOSTS رو درست تنظیم کردم
- [ ] پسورد دیتابیس رو تغییر دادم
- [ ] OPENROUTER_API_KEY رو گرفتم و گذاشتم
- [ ] CORS_ALLOW_ALL_ORIGINS=False کردم
- [ ] CORS_ALLOWED_ORIGINS رو با دامنه فرانت‌اند تنظیم کردم
- [ ] DB_PASSWORD رو در .env اضافه کردم
- [ ] فایل .env رو به گیت commit نکردم (.gitignore چک کردم)

### بعد از دیپلوی:
- [ ] همه سرویس‌ها running هستن
- [ ] مایگریشن‌ها اجرا شدن
- [ ] collectstatic اجرا شد
- [ ] superuser ساختم
- [ ] populate_features اجرا شد
- [ ] endpoint /health جواب می‌ده
- [ ] API ها کار می‌کنن
- [ ] می‌تونم login کنم
- [ ] می‌تونم reading بسازم

### امنیت:
- [ ] پسوردهای پیش‌فرض عوض شدن
- [ ] فایروال فعاله
- [ ] فقط پورت‌های لازم باز هستن (22, 80, 443)
- [ ] SSL نصب شد (اگه دامنه داری)

---

## 🆘 مشکلات متداول

### مشکل: سرویس‌ها start نمی‌شن
```bash
# لاگ‌ها رو ببین
docker-compose -f docker-compose.prod.yml logs

# یک سرویس خاص
docker-compose -f docker-compose.prod.yml logs web
```

### مشکل: خطای دیتابیس
```bash
# چک کن دیتابیس healthy باشه
docker-compose -f docker-compose.prod.yml ps db

# ریستارت دیتابیس
docker-compose -f docker-compose.prod.yml restart db

# دوباره مایگریشن
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### مشکل: 502 Bad Gateway از nginx
```bash
# چک کن web service در حال اجراست
docker-compose -f docker-compose.prod.yml ps web

# لاگ web
docker-compose -f docker-compose.prod.yml logs web

# ریستارت
docker-compose -f docker-compose.prod.yml restart web nginx
```

### مشکل: OPENROUTER_API_KEY کار نمی‌کنه
```bash
# چک کن در .env درست هست
cat .env | grep OPENROUTER

# ریستارت سرویس‌ها تا env جدید بخونن
docker-compose -f docker-compose.prod.yml restart
```

---

## 📞 منابع و لینک‌های مفید

- **راهنمای کامل VPS**: [VPS_DEPLOYMENT.md](VPS_DEPLOYMENT.md)
- **مستندات API**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **راهنمای فارسی**: [PERSIAN_API_GUIDE.md](PERSIAN_API_GUIDE.md)
- **OpenRouter Dashboard**: https://openrouter.ai/dashboard
- **OpenRouter Keys**: https://openrouter.ai/keys
- **Let's Encrypt**: https://letsencrypt.org/

---

## 🎉 تمام شد!

اگه همه چک‌باکس‌ها تیک خوردن، پروژه‌ت آماده production است! 🚀

برای مانیتورینگ و نگهداری، حتماً لاگ‌ها رو چک کن:
```bash
docker-compose -f docker-compose.prod.yml logs -f
```
