# VPS Deployment Guide - Coffee Fortune Server

This guide will help you deploy the Coffee Fortune Server on a VPS (Virtual Private Server) with nginx as a reverse proxy.

## Prerequisites

### VPS Requirements
- Ubuntu 20.04 or 22.04 (recommended)
- Minimum 2GB RAM (4GB recommended)
- 20GB storage minimum
- Root or sudo access
- Public IP address

### Domain Setup (Optional but Recommended)
- Domain name pointing to your VPS IP
- DNS A record configured (e.g., `api.yourdomain.com` -> `YOUR_VPS_IP`)

## Step 1: Initial VPS Setup

### Connect to Your VPS
```bash
ssh root@YOUR_VPS_IP
# or
ssh your-username@YOUR_VPS_IP
```

### Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Required Software
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Install Git
sudo apt install git -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional, to run docker without sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

### Configure Firewall
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

## Step 2: Clone and Setup Project

### Clone Repository
```bash
cd /home/$USER
git clone <your-repository-url> coffee-fortune-server
cd coffee-fortune-server
```

### Create Environment File
```bash
cp .env.example .env
nano .env
```

### Configure Production Environment Variables
Edit `.env` file with production settings:

```env
# Django Settings
SECRET_KEY=<generate-a-strong-secret-key-here>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,YOUR_VPS_IP

# Database (using Docker PostgreSQL)
DATABASE_URL=postgresql://postgres:CHANGE_THIS_PASSWORD@db:5432/coffee_fortune_db

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

# OpenRouter AI API
OPENROUTER_API_KEY=your-openrouter-api-key-here

# OTP Configuration
OTP_EXPIRY_SECONDS=120
SMS_API_KEY=your-sms-provider-api-key

# CORS (add your frontend domains)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**IMPORTANT Security Notes:**
- Generate a strong SECRET_KEY (use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- Change database password from default
- Set DEBUG=False for production
- Update ALLOWED_HOSTS with your actual domain
- Never commit `.env` to git

### Update docker-compose for Production
```bash
nano docker-compose.yml
```

Update the database password in the `db` service and `web`, `celery`, `celery-beat` services to match your `.env` file.

## Step 3: Configure Nginx for Your Domain

### Update Nginx Configuration
```bash
nano nginx/nginx.conf
```

Replace `server_name _;` with your actual domain:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

## Step 4: Build and Start Services

### Build Docker Images
```bash
docker-compose build
```

### Start Services
```bash
docker-compose up -d
```

### Check Services Status
```bash
docker-compose ps
```

All services should show as "running" or "healthy".

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f nginx
```

## Step 5: Initialize Application

### Run Database Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Populate Fortune Features
```bash
docker-compose exec web python manage.py populate_features
```

## Step 6: Setup SSL Certificate (HTTPS)

### Install Certbot
```bash
# On your VPS (not inside Docker)
sudo apt install certbot python3-certbot-nginx -y
```

### Stop Nginx Container Temporarily
```bash
docker-compose stop nginx
```

### Obtain SSL Certificate
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts and provide your email address.

### Update Nginx Configuration for SSL
```bash
nano nginx/nginx.conf
```

Uncomment the HTTPS server block and update:
```nginx
server_name yourdomain.com www.yourdomain.com;
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

Also uncomment the HTTP redirect in the first server block:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Update docker-compose.yml for SSL
```bash
nano docker-compose.yml
```

Uncomment the SSL certificate volumes in the nginx service:
```yaml
volumes:
  - ./staticfiles:/app/staticfiles
  - ./media:/app/media
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

### Restart Nginx
```bash
docker-compose up -d nginx
```

### Setup SSL Auto-Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot will automatically renew certificates
# Verify cron job exists
sudo systemctl status certbot.timer
```

## Step 7: Verify Deployment

### Test HTTP/HTTPS Access
```bash
curl http://yourdomain.com/health
curl https://yourdomain.com/health
```

Both should return "healthy".

### Test API Endpoints
```bash
# Get features
curl https://yourdomain.com/api/fortune/features/

# Check admin panel
# Visit: https://yourdomain.com/admin
```

### Monitor Logs
```bash
# Watch logs in real-time
docker-compose logs -f

# Check for errors
docker-compose logs web | grep ERROR
docker-compose logs celery | grep ERROR
```

## Step 8: Production Optimizations

### Setup Log Rotation
Create `/etc/logrotate.d/docker-coffee-fortune`:
```bash
sudo nano /etc/logrotate.d/docker-coffee-fortune
```

Add:
```
/home/youruser/coffee-fortune-server/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
```

### Setup Monitoring Script
Create monitoring script:
```bash
nano ~/monitor.sh
```

Add:
```bash
#!/bin/bash
cd /home/$USER/coffee-fortune-server
docker-compose ps | grep -q "Exit\|unhealthy" && docker-compose restart
```

Make executable and add to cron:
```bash
chmod +x ~/monitor.sh
crontab -e
# Add: */5 * * * * /home/youruser/monitor.sh
```

### Database Backups
Create backup script:
```bash
nano ~/backup-db.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/home/$USER/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cd /home/$USER/coffee-fortune-server
docker-compose exec -T db pg_dump -U postgres coffee_fortune_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

Make executable and schedule:
```bash
chmod +x ~/backup-db.sh
crontab -e
# Add: 0 2 * * * /home/youruser/backup-db.sh
```

## Managing the Application

### Update Application Code
```bash
cd /home/$USER/coffee-fortune-server
git pull origin main
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### Restart Services
```bash
docker-compose restart
```

### Stop Services
```bash
docker-compose down
```

### View Resource Usage
```bash
docker stats
```

### Clean Up Old Images
```bash
docker system prune -a
```

## Troubleshooting

### Check Service Status
```bash
docker-compose ps
docker-compose logs service-name
```

### Common Issues

#### Issue: Port 80/443 already in use
```bash
# Check what's using the port
sudo lsof -i :80
sudo lsof -i :443

# Stop conflicting service (e.g., Apache)
sudo systemctl stop apache2
sudo systemctl disable apache2
```

#### Issue: Database connection errors
```bash
# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

#### Issue: Permission errors with volumes
```bash
# Fix permissions
sudo chown -R $USER:$USER ./staticfiles ./media
chmod -R 755 ./staticfiles ./media
```

#### Issue: Nginx 502 Bad Gateway
```bash
# Check if web service is running
docker-compose ps web

# Check web service logs
docker-compose logs web

# Restart services
docker-compose restart web nginx
```

#### Issue: SSL certificate not working
```bash
# Verify certificate exists
sudo ls -la /etc/letsencrypt/live/yourdomain.com/

# Check nginx configuration
docker-compose exec nginx nginx -t

# Renew certificate manually
sudo certbot renew --force-renewal
docker-compose restart nginx
```

## Security Checklist

- [ ] Changed default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Changed database password
- [ ] Configured ALLOWED_HOSTS
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured (UFW)
- [ ] Regular backups scheduled
- [ ] Log rotation configured
- [ ] Updated all default passwords
- [ ] Restricted database port (not exposed publicly)
- [ ] Configured CORS properly
- [ ] SSH key authentication enabled
- [ ] Disabled root SSH login (optional)
- [ ] Setup monitoring

## Performance Tuning

### For High Traffic (4GB+ RAM VPS)

Update `docker-compose.yml` web service command:
```yaml
command: gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 2 --timeout 300 config.wsgi:application
```

### Database Connection Pooling

Add to `.env`:
```env
DB_CONN_MAX_AGE=600
```

### Redis Memory Limit

Add to redis service in `docker-compose.yml`:
```yaml
redis:
  image: redis:7-alpine
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

## Monitoring and Logs

### Access Logs
```bash
# Nginx access logs
docker-compose exec nginx cat /var/log/nginx/access.log

# Application logs
docker-compose logs web

# Celery worker logs
docker-compose logs celery
```

### Monitor System Resources
```bash
# CPU and memory usage
htop

# Disk usage
df -h

# Docker stats
docker stats
```

## Scaling (Optional)

For high traffic, consider:
1. Use managed database (e.g., AWS RDS, Digital Ocean Managed Database)
2. Use managed Redis (e.g., Redis Cloud, AWS ElastiCache)
3. Deploy multiple VPS instances behind a load balancer
4. Use CDN for static files
5. Implement caching (Redis cache backend)

## Support

For issues:
- Check logs: `docker-compose logs`
- Review Django settings
- Check OpenRouter API status
- Verify environment variables

## Useful Commands Reference

```bash
# View all containers
docker-compose ps

# Restart a specific service
docker-compose restart web

# View real-time logs
docker-compose logs -f web

# Execute command in container
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec db psql -U postgres coffee_fortune_db

# Redis CLI
docker-compose exec redis redis-cli

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Next Steps

1. Configure your SMS provider for OTP delivery
2. Setup monitoring (e.g., UptimeRobot, Prometheus)
3. Configure backup strategy
4. Setup CI/CD pipeline (optional)
5. Configure domain email for SSL notifications
6. Test all API endpoints
7. Load test your application
8. Document your API for frontend team

Your Coffee Fortune Server is now deployed and ready for production use!
