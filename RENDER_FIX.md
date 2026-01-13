# Render Deployment - Quick Fix Guide

## Issue: Database Configuration Error

The deployment failed because of database configuration. Here are two solutions:

---

## ✅ Solution 1: Use SQLite (Simplest)

**Note**: Data will be lost when the service restarts on Render's free tier.

### Update `render.yaml`:

```yaml
envVars:
  - key: DATABASE_URL
    value: sqlite+aiosqlite:////opt/render/project/src/vid_system.db
```

This is already set in the updated `render.yaml`.

---

## ✅ Solution 2: Use PostgreSQL (Recommended for Production)

**Persistent data** - survives restarts.

### Step 1: Create PostgreSQL Database on Render

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name: `vid-system-db`
4. Plan: **Free**
5. Click "Create Database"
6. Copy the **Internal Database URL**

### Step 2: Update Backend Requirements

Add to `backend/requirements.txt`:
```
asyncpg>=0.29.0
```

### Step 3: Update Environment Variable

In your Render Web Service:
1. Go to "Environment" tab
2. Update `DATABASE_URL` to your PostgreSQL Internal URL
3. Format: `postgresql+asyncpg://user:pass@host/dbname`
4. Save changes

### Step 4: Redeploy

Render will automatically redeploy with the new configuration.

---

## 🚀 Quick Deploy with SQLite

The current configuration uses SQLite. Just push your changes:

```bash
git add .
git commit -m "Fix Render deployment configuration"
git push
```

Render will auto-deploy and should work now!

---

## 🔍 Verify Deployment

Once deployed, check:

1. **Health Check**: `https://your-app.onrender.com/health`
2. **API Docs**: `https://your-app.onrender.com/docs`
3. **Root**: `https://your-app.onrender.com/`

Should return:
```json
{
  "message": "Privacy-Preserving Virtual Identity System",
  "version": "1.0.0",
  "status": "operational"
}
```

---

## ⚠️ Important Notes

### SQLite on Render Free Tier:
- ✅ Works immediately
- ✅ No additional setup
- ⚠️ Data lost on service restart
- ⚠️ Service sleeps after 15 min inactivity

### PostgreSQL on Render Free Tier:
- ✅ Persistent data
- ✅ Survives restarts
- ✅ Better for production
- ⚠️ Requires additional setup
- ⚠️ Free tier: 90 days, then $7/month

---

## 📝 Current Status

Your `render.yaml` is now configured for **SQLite** with the correct path for Render's filesystem.

**Next step**: Push to GitHub and Render will auto-deploy!
