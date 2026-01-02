# CausalityCare Backend - Deployment Guide

This guide covers deploying the CausalityCare API backend to Railway with full production configuration.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Railway Setup](#railway-setup)
3. [Environment Configuration](#environment-configuration)
4. [Deployment Process](#deployment-process)
5. [Health Checks & Monitoring](#health-checks--monitoring)
6. [Database Management](#database-management)
7. [Troubleshooting](#troubleshooting)
8. [Performance Tuning](#performance-tuning)

## Prerequisites

### Required
- Railway account ([Sign up here](https://railway.app))
- GitHub repository with the CausalityCare code
- Google Gemini API key ([Create one](https://ai.google.dev))
- Domain name (optional, for custom URLs)

### Files
- `Dockerfile` - Container configuration
- `railway.json` - Railway-specific settings
- `requirements.txt` - Python dependencies

## Railway Setup

### Step 1: Connect GitHub Repository

1. Log in to [Railway Dashboard](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your GitHub account and the `causalitycare` repository
4. Choose the deployment strategy:
   - **Auto-deploy on push**: Recommended (auto-deploys on git push)
   - **Manual deploy**: Deploy when you trigger it

### Step 2: Create a Railway Project

1. Name your project: `causalitycare` or `causalitycare-backend`
2. Select the starter plan (auto-scales as needed)
3. Railway will auto-detect the `Dockerfile`

### Step 3: Configure Services

#### Automatic Detection
Railway will automatically:
- Detect the Dockerfile
- Build the container
- Expose port 8000
- Run the application

#### Manual Configuration (if needed)
In Railway dashboard:
1. Go to **Settings**
2. Set **Root Directory** to `backend` (if not auto-detected)
3. Ensure **Build Command** matches your Dockerfile
4. Set **Start Command** to `python main.py`

## Environment Configuration

### Required Environment Variables

Add these to Railway **Variables** section:

```
GEMINI_API_KEY=<your-google-gemini-api-key>
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=sqlite:///./causalitycare.db
API_HOST=0.0.0.0
API_PORT=8000
```

### Setting Variables in Railway

1. Go to your Railway project
2. Click **Settings**
3. Scroll to **Variables**
4. Add each variable as a key-value pair:

| Key | Value | Sensitive |
|-----|-------|-----------|
| `GEMINI_API_KEY` | Your API key | ✅ Yes |
| `ENVIRONMENT` | `production` | ❌ No |
| `DEBUG` | `false` | ❌ No |
| `API_PORT` | `8000` | ❌ No |

### Handling Sensitive Variables

1. For `GEMINI_API_KEY`, Railway will automatically treat it as sensitive
2. The value won't be visible in logs or the UI after saving
3. Use the 🔐 lock icon to manage sensitivity

## Deployment Process

### Automatic Deployment

Once connected, Railway will:

1. **Watch** your repository for changes
2. **Build** the Docker image when you push to `main`/`develop`
3. **Run** health checks
4. **Auto-restart** on failure

```bash
# Your local workflow
git add .
git commit -m "Update API configuration"
git push origin main

# Railway automatically:
# 1. Detects the push
# 2. Builds the Dockerfile
# 3. Runs the new container
# 4. Performs health checks
# 5. Routes traffic if healthy
```

### Manual Deployment

If auto-deploy is disabled:

1. Go to Railway Dashboard
2. Select your service
3. Click **Redeploy** to manually trigger a build

### Monitoring Deployment

In Railway Dashboard:
1. Click **Logs** to see real-time logs
2. Watch for the startup message:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```
3. Check **Deployments** tab for history

## Health Checks & Monitoring

### Built-in Health Check Endpoint

The application includes a `/health` endpoint:

```bash
curl https://your-deployment.up.railway.app/health
# Response: 200 OK
```

### Docker HEALTHCHECK Configuration

The Dockerfile includes automated health checks:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1
```

**Behavior**:
- Checks every **30 seconds**
- Waits up to **10 seconds** for response
- Allows **5 seconds** startup grace period
- Restarts after **3 failed checks** (90 seconds total)

### Railway Health Monitoring

1. **View Status**: Dashboard → **Status** tab
2. **Check Uptime**: Shows deployment history
3. **View Metrics**: CPU, Memory, Network usage
4. **Set Alerts**: Configure notifications for failures

### Custom Monitoring (Optional)

For production, consider adding:
- **Sentry**: Error tracking (`pip install sentry-sdk`)
- **DataDog**: Performance monitoring
- **New Relic**: Application performance monitoring

## Database Management

### SQLite (Current Setup)

**Pros**:
- Zero configuration
- Great for MVP/prototyping
- File-based persistence

**Cons**:
- Not suitable for high concurrency
- Limited scaling

**Location**: Railway mounted volume at `./causalitycare.db`

### Upgrading to PostgreSQL

For production with high traffic:

1. **Add PostgreSQL service**:
   ```bash
   # In Railway dashboard, click "+ Add Service" → PostgreSQL
   ```

2. **Get connection string**:
   ```
   postgresql://user:password@host:5432/railway
   ```

3. **Update Railway variable**:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/railway
   ```

4. **Update local dev**:
   ```bash
   # .env
   DATABASE_URL=postgresql://localhost/causalitycare
   ```

5. **Install driver**:
   ```bash
   pip install psycopg2-binary
   # Add to requirements.txt
   ```

### Database Migrations

If using SQLAlchemy migrations (Alembic):

```bash
# In Dockerfile, before running app:
RUN alembic upgrade head

# Update CMD:
CMD alembic upgrade head && python main.py
```

## Troubleshooting

### Deployment Fails to Build

**Issue**: Docker build fails
```
ERROR: failed to build image
```

**Solutions**:
1. Check Railway **Logs** for specific error
2. Verify `Dockerfile` is in repository root (or `backend/` folder)
3. Ensure `requirements.txt` is valid Python packages
4. Check Docker syntax:
   ```bash
   docker build -f Dockerfile -t test .
   ```

### Application Crashes on Startup

**Issue**: Container starts then stops
```
Health check failed after retries
```

**Solutions**:
1. Verify `GEMINI_API_KEY` is set
2. Check startup logs for errors:
   ```bash
   # In Railway, click service → Logs
   ```
3. Verify Python version: `python:3.9-slim`
4. Test locally:
   ```bash
   docker run -e GEMINI_API_KEY=test causalitycare-backend
   ```

### 502 Bad Gateway

**Issue**: Request returns 502
```
<html><body><h1>502 Bad Gateway</h1></body></html>
```

**Solutions**:
1. Check if application is running: `https://.../health`
2. Verify port 8000 is exposed in Dockerfile
3. Check Railway **Metrics** for crashes
4. Review recent logs for errors

### Health Check Timeout

**Issue**: Container keeps restarting
```
HEALTHCHECK: timeout
```

**Solutions**:
1. Increase `start-period` in Dockerfile if startup is slow
2. Check API is responding: Try accessing `/health` manually
3. Verify network connectivity from container
4. Check for infinite loops in startup code

### Database Locked

**Issue**: SQLite database is locked
```
sqlite3.OperationalError: database is locked
```

**Solutions**:
1. Upgrade to PostgreSQL (recommended for production)
2. Reduce concurrent connections
3. Add retry logic to database queries
4. Use WAL mode in SQLite:
   ```python
   # In database.py
   engine = create_engine(
       settings.database_url,
       connect_args={"timeout": 15},
       pool_pre_ping=True
   )
   ```

## Performance Tuning

### Uvicorn Workers

By default, the app runs with 1 worker. For better throughput:

```python
# main.py: Update startup
if __name__ == "__main__":
    import uvicorn
    workers = 4  # Adjust based on available CPU cores
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=workers
    )
```

### Request Timeouts

Adjust in `main.py`:
```python
IMAGE_PROCESSING_TIMEOUT = 30   # Increase if images are large
AUDIO_PROCESSING_TIMEOUT = 40   # Increase for long audio files
TEXT_PROCESSING_TIMEOUT = 20    # Gemini response time
```

### Database Connection Pooling

Configure in `database.py`:
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,           # Connections to keep open
    max_overflow=20,        # Additional connections when needed
    pool_pre_ping=True      # Verify connections before use
)
```

### Caching

Add Redis for caching common queries:

```bash
# Install
pip install redis

# In Railway, add Redis service
# Set variable: REDIS_URL=redis://user:pass@host:6379
```

## Monitoring & Logs

### View Real-time Logs

```bash
# In Railway Dashboard:
# Service → Logs tab
```

### Log Aggregation

Export logs to external service:
- **Datadog**: Install agent, push logs
- **CloudWatch**: Use AWS integration
- **Sentry**: Auto-capture exceptions

### Scaling

As traffic grows:

1. **Railway auto-scaling**: Automatically scales instances
2. **Monitor usage**: Watch CPU/Memory in Dashboard
3. **Upgrade plan**: Go from Starter → Pro for more resources
4. **Add CDN**: Use Cloudflare for static content caching

## Security Best Practices

1. ✅ **Secrets Management**: Railway handles sensitive variables
2. ✅ **HTTPS**: Railway provides free SSL/TLS
3. ✅ **Database**: Use PostgreSQL with encryption
4. ⚠️ **CORS**: Currently allows all origins. Restrict in production:
   ```python
   allow_origins=[
       "https://yourdomain.com",
       "https://www.yourdomain.com"
   ]
   ```
5. ⚠️ **Rate Limiting**: Add for production
   ```bash
   pip install slowapi
   ```

## Custom Domain

To use your own domain:

1. **In Railway Dashboard**:
   - Settings → Domains
   - Click "Add Domain"
   - Enter your domain: `api.yourdomain.com`

2. **Update DNS**:
   - Get the CNAME from Railway
   - Add to DNS provider (Cloudflare, Route53, etc.)

3. **SSL Certificate**:
   - Railway auto-provisions Let's Encrypt certificate
   - HTTPS enabled by default

## Rollback & Deployment History

### View Deployment History

1. Dashboard → **Deployments** tab
2. Click on any deployment to view details
3. Shows timestamp, status, and logs

### Rollback to Previous Version

1. **Deployments** tab
2. Find the stable deployment
3. Click **Redeploy** next to it
4. Confirms rollback

### Create Stable Versions

Use Git tags for important versions:
```bash
git tag v2.1.0-prod
git push origin v2.1.0-prod
# Reference in Railway deploy notes
```

## Disaster Recovery

### Backup Strategy

1. **Database Backups**:
   - If using PostgreSQL, enable automated backups in Railway
   - Export SQLite database periodically:
     ```bash
     scp railway:/app/causalitycare.db ./backup/
     ```

2. **Code Backups**:
   - GitHub is your backup (all commits stored)
   - Tag important releases

3. **Configuration Backup**:
   - Document all Railway variables in `.env.example`
   - Keep Git history clean

### Disaster Recovery Plan

1. **Service Down**: Click **Redeploy** in Railway
2. **Data Loss**: Restore from database backup
3. **Code Issues**: Rollback to previous deployment

---

**Version**: 2.1.0  
**Last Updated**: January 2, 2025  
**Deployment Platform**: Railway
